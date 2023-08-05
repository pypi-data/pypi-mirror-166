from __future__ import annotations

import importlib
import logging
import os
import re
import subprocess
import textwrap
import warnings
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from setuptools.dist import Distribution

if TYPE_CHECKING:
    from packaging.version import Version

DEFAULT_TEMPLATE = "{tag}"
DEFAULT_DEV_TEMPLATE = "{tag}.post{ccount}+git.{sha}"
DEFAULT_DIRTY_TEMPLATE = "{tag}.post{ccount}+git.{sha}.dirty"
DEFAULT_STARTING_VERSION = "0.0.1"
DEFAULT_SORT_BY = "creatordate"
ENV_VARS_REGEXP = re.compile(r"\{env:(?P<name>[^:}]+):?(?P<default>[^}]+\}*)?\}", re.IGNORECASE | re.UNICODE)
TIMESTAMP_REGEXP = re.compile(r"\{timestamp:?(?P<fmt>[^:}]+)?\}", re.IGNORECASE | re.UNICODE)
LOCAL_REGEXP = re.compile(r"[^a-z\d.]+", re.IGNORECASE)
VERSION_PREFIX_REGEXP = re.compile(r"^[^\d]+", re.IGNORECASE | re.UNICODE)

DEFAULT_CONFIG = {
    "template": DEFAULT_TEMPLATE,
    "dev_template": DEFAULT_DEV_TEMPLATE,
    "dirty_template": DEFAULT_DIRTY_TEMPLATE,
    "starting_version": DEFAULT_STARTING_VERSION,
    "version_callback": None,
    "version_file": None,
    "count_commits_from_version_file": False,
    "tag_formatter": None,
    "branch_formatter": None,
    "sort_by": DEFAULT_SORT_BY,
}

log = logging.getLogger(__name__)


def _exec(cmd: str) -> list[str]:
    try:
        stdout = subprocess.check_output(cmd, shell=True, text=True)  # nosec
    except subprocess.CalledProcessError as e:
        stdout = e.output
    lines = stdout.splitlines()
    return [line.rstrip() for line in lines if line.rstrip()]


def get_branches() -> list[str]:
    branches = _exec("git branch -l --format '%(refname:short)'")
    if branches:
        return branches
    return []


def get_branch() -> str | None:
    branches = _exec("git rev-parse --abbrev-ref HEAD")
    if branches:
        return branches[0]
    return None


def get_all_tags(sort_by: str = DEFAULT_SORT_BY) -> list[str]:
    tags = _exec(f"git tag --sort=-{sort_by}")
    if tags:
        return tags
    return []


def get_branch_tags(*args, **kwargs) -> list[str]:
    warnings.warn(
        "`get_branch_tags` function is deprecated "
        "since setuptools-git-versioning v1.8.0 "
        "and will be dropped in v2.0.0\n"
        "Please use `get_tags` instead",
        category=UserWarning,
    )

    return get_tags(*args, **kwargs)


def get_tags(sort_by: str = DEFAULT_SORT_BY) -> list[str]:
    tags = _exec(f"git tag --sort=-{sort_by} --merged")
    if tags:
        return tags
    return []


def get_tag(*args, **kwargs) -> str | None:
    tags = get_tags(*args, **kwargs)
    if tags:
        return tags[0]
    return None


def get_sha(name: str = "HEAD") -> str | None:
    sha = _exec(f'git rev-list -n 1 "{name}"')
    if sha:
        return sha[0]
    return None


def get_latest_file_commit(path: str | os.PathLike) -> str | None:
    file_path = Path(path)
    sha = _exec(f'git log -n 1 --pretty=format:%H -- "{file_path}"')
    if sha:
        return sha[0]
    return None


def is_dirty() -> bool:
    res = _exec("git status --short")
    if res:
        return True
    return False


def count_since(name: str) -> int | None:
    res = _exec(f'git rev-list --count HEAD "^{name}"')
    if res:
        return int(res[0])
    return None


def load_config_from_dict(dictionary: Mapping) -> dict:
    config = {}
    for key, value in DEFAULT_CONFIG.items():
        config[key] = dictionary.get(key, value)
    return config


def read_toml(file_name: str | os.PathLike) -> dict:
    file_path = Path(file_name)
    if not file_path.exists() or not file_path.is_file():
        return {}

    import toml

    parsed_file = toml.load(file_path)

    return parsed_file.get("tool", {}).get("setuptools-git-versioning", None)


# TODO: remove along with version_config
def parse_config(dist: Distribution, attr: Any, value: Any) -> None:
    from distutils.errors import DistutilsOptionError

    if attr == "version_config" and value is not None:
        warnings.warn(
            "`version_config` option is deprecated "
            "since setuptools-git-versioning v1.8.0 "
            "and will be dropped in v2.0.0\n"
            "Please rename it to `setuptools_git_versioning`",
            category=UserWarning,
        )

        if getattr(dist, "setuptools_git_versioning", None) is not None:
            raise DistutilsOptionError(
                "You can set either `version_config` or `setuptools_git_versioning` "
                "but not both of them at the same time"
            )


# real version is generated here
def infer_version(dist: Distribution) -> None:
    from distutils.errors import DistutilsOptionError, DistutilsSetupError

    value = getattr(dist, "setuptools_git_versioning", None) or getattr(dist, "version_config", None)

    if isinstance(value, bool):
        warnings.warn(
            "Passing boolean value to `version_config`/`setuptools_git_versioning` option is deprecated "
            "since setuptools-git-versioning 1.8.0 "
            "and will be dropped in v2.0.0\n"
            "Please change value to `{'enabled': False/True}`",
            category=UserWarning,
        )
        value = {"enabled": value}

    toml_value = read_toml("pyproject.toml")

    if value is None:
        value = toml_value
    elif toml_value:
        raise DistutilsSetupError(
            "Both setup.py and pyproject.toml have setuptools-git-versioning config. Please remove one of them"
        )

    if value is None:
        # Nothing to do here
        return

    if not isinstance(value, Mapping):
        raise DistutilsOptionError(f"Wrong config format. Expected dict, got: {value}")

    if not value or not value.get("enabled", True):
        # Nothing to do here
        return

    config = load_config_from_dict(value)

    version = version_from_git(dist.metadata.name, **config)
    dist.metadata.version = version


def read_version_from_file(path: str | os.PathLike) -> str:
    return Path(path).read_text().strip()


def substitute_env_variables(template: str) -> str:
    for var, default in ENV_VARS_REGEXP.findall(template):
        if default.upper() == "IGNORE":
            default = ""
        elif not default:
            default = "UNKNOWN"

        value = os.environ.get(var, default)
        template, _ = ENV_VARS_REGEXP.subn(value, template, count=1)

    return template


def substitute_timestamp(template: str) -> str:
    now = datetime.now()
    for fmt in TIMESTAMP_REGEXP.findall(template):
        result = now.strftime(fmt or "%s")
        template, _ = TIMESTAMP_REGEXP.subn(result, template, count=1)

    return template


def resolve_substitutions(template: str, *args, **kwargs) -> str:
    while True:
        if "{env" in template:
            new_template = substitute_env_variables(template)
            if new_template == template:
                break
            else:
                template = new_template
        else:
            break

    if "{timestamp" in template:
        template = substitute_timestamp(template)

    return template.format(*args, **kwargs)


def import_reference(
    ref: str,
    package_name: str | None = None,
) -> Any:
    if ":" not in ref:
        raise NameError(f"Wrong reference name: {ref}")

    module_name, attr = ref.split(":")
    module = importlib.import_module(module_name, package_name)

    return getattr(module, attr)


def load_callable(
    inp: str,
    package_name: str | None = None,
) -> Callable:

    ref = import_reference(inp, package_name)
    if not callable(ref):
        raise ValueError(f"{ref} of type {type(ref)} is not callable")

    return ref


def load_tag_formatter(
    tag_formatter: str | Callable[[str], str],
    package_name: str | None = None,
) -> Callable:
    log.warning(f"Parsing tag_formatter {tag_formatter} with type {type(tag_formatter)}")

    if callable(tag_formatter):
        return tag_formatter

    try:
        return load_callable(tag_formatter, package_name)
    except (ImportError, NameError) as e:
        log.warning(f"tag_formatter is not a valid function reference:\n\t{e}")

    try:
        pattern = re.compile(tag_formatter)

        def formatter(tag):
            match = pattern.match(tag)
            if match:
                return match.group("tag")

            raise ValueError(f"Tag name {tag} does not match regexp '{tag_formatter}'")

        return formatter
    except re.error as e:
        log.warning(f"tag_formatter is not valid regexp:\n\t{e}")

    raise ValueError("Cannot parse tag_formatter")


def load_branch_formatter(
    branch_formatter: str | Callable[[str], str],
    package_name: str | None = None,
) -> Callable:
    log.warning(
        "Parsing branch_formatter {branch_formatter} with type {type}".format(
            branch_formatter=branch_formatter,
            type=type(branch_formatter),
        )
    )

    if callable(branch_formatter):
        return branch_formatter

    try:
        return load_callable(branch_formatter, package_name)
    except (ImportError, NameError) as e:
        log.warning(f"branch_formatter is not a valid function reference:\n\t{e}")

    try:
        pattern = re.compile(branch_formatter)

        def formatter(branch):
            match = pattern.match(branch)
            if match:
                return match.group("branch")

            raise ValueError(f"Branch name {branch} does not match regexp '{branch_formatter}'")

        return formatter
    except re.error as e:
        log.warning(f"branch_formatter is not valid regexp:\n\t{e}")

    raise ValueError("Cannot parse branch_formatter")


# TODO: return Version object instead of str
def get_version_from_callback(
    version_callback: str | Callable[[], str],
    package_name: str | None = None,
) -> str:
    log.warning(f"Parsing version_callback {version_callback} with type {type(version_callback)}")

    if callable(version_callback):
        result = version_callback()
    else:
        result = version_callback

        try:
            result = load_callable(version_callback, package_name)()
        except ValueError:
            result = import_reference(version_callback, package_name)
        except (ImportError, NameError) as e:
            log.warning(f"version_callback is not a valid reference:\n\t{e}")

    from packaging.version import Version

    return Version(result).public


# TODO: return Version object instead of str
def version_from_git(
    package_name: str | None = None,
    template: str = DEFAULT_TEMPLATE,
    dev_template: str = DEFAULT_DEV_TEMPLATE,
    dirty_template: str = DEFAULT_DIRTY_TEMPLATE,
    starting_version: str = DEFAULT_STARTING_VERSION,
    version_callback: str | Callable[[], str] | None = None,
    version_file: str | os.PathLike | None = None,
    count_commits_from_version_file: bool = False,
    tag_formatter: Callable[[str], str] | None = None,
    branch_formatter: Callable[[str], str] | None = None,
    sort_by: str = DEFAULT_SORT_BY,
) -> str:
    # Check if PKG-INFO file exists and Version is present in it
    if os.path.exists("PKG-INFO"):
        with open("PKG-INFO") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("Version:"):
                return line[8:].strip()

    if version_callback is not None:
        if version_file is not None:
            raise ValueError(
                "Either `version_file` or `version_callback` can be passed, but not both at the same time",
            )
        return get_version_from_callback(version_callback, package_name)

    from_file = False
    tag = get_tag(sort_by=sort_by)

    if tag is None:
        if version_file is None or not os.path.exists(version_file):
            return starting_version
        else:
            from_file = True
            tag = read_version_from_file(version_file)

            if not tag:
                return starting_version

            if not count_commits_from_version_file:
                return VERSION_PREFIX_REGEXP.sub("", tag)  # for tag "v1.0.0" drop leading "v" symbol

            tag_sha = get_latest_file_commit(version_file)
    else:
        tag_sha = get_sha(tag)

        if tag_formatter is not None:
            tag_fmt = load_tag_formatter(tag_formatter, package_name)
            tag = tag_fmt(tag)

    dirty = is_dirty()
    head_sha = get_sha()
    full_sha = head_sha if head_sha is not None else ""
    ccount = count_since(tag_sha) if tag_sha is not None else None
    on_tag = head_sha is not None and head_sha == tag_sha and not from_file

    branch = get_branch()
    if branch_formatter is not None and branch is not None:
        branch_fmt = load_branch_formatter(branch_formatter, package_name)
        branch = branch_fmt(branch)

    if dirty:
        t = dirty_template
    elif not on_tag and ccount is not None:
        t = dev_template
    else:
        t = template

    version = resolve_substitutions(t, sha=full_sha[:8], tag=tag, ccount=ccount, branch=branch, full_sha=full_sha)

    # Ensure local version label only contains permitted characters
    public, sep, local = version.partition("+")
    local_sanitized = LOCAL_REGEXP.sub(".", local)
    public_sanitized = VERSION_PREFIX_REGEXP.sub("", public)  # for version "v1.0.0" drop leading "v" symbol
    return public_sanitized + sep + local_sanitized


def main(config: dict | None = None) -> Version:
    value = config or read_toml("pyproject.toml")

    if not value or not value.get("enabled", True):
        raise RuntimeError(
            textwrap.dedent(
                """
                'setuptools-git-versioning' command can be used only with 'pyproject.toml'
                file setup (see https://setuptools-git-versioning.readthedocs.io/en/stable/install.html)
                """,
            ),
        )

    if not isinstance(value, Mapping):
        raise RuntimeError(f"Wrong config format. Expected dict, got: {value}")

    config = load_config_from_dict(value)
    result = version_from_git(**config)

    from packaging.version import Version

    return Version(result)


def __main__():
    print(main().public)


if __name__ == "__main__":
    __main__()
