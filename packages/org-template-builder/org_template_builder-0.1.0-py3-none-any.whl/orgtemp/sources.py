"""
Default install sources from strings or remote urls.
This will execute requests to get text from files.
"""
from pathlib import Path
import re
import requests


LICENSE = "https://www.gnu.org/licenses/gpl-3.0.txt"
MAKEFILE = "https://albertovaldez5.gitlab.io/org-template/resources/Makefile"
GITIGNORE = "https://albertovaldez5.gitlab.io/org-template/resources/.gitignore"
SM_CONFIG = "git@gitlab.com:albertovaldez5/org-config.git"
SM_THEME = "git@gitlab.com:albertovaldez5/org-theme.git"


class Directories:
    """Directories at the root level."""

    docs = Path("docs")
    public = Path("public")
    resources = Path("resources")
    src = Path("src")
    tests = Path("tests")

    def __iter__(self):
        return iter([self.docs, self.public, self.resources, self.src, self.tests])


directories = Directories()


def get_makefile(name: str):
    r = requests.get(MAKEFILE).text
    return re.sub("PROJECT_NAME = org-template", f"PROJECT_NAME = {name}", r)


def get_root_files() -> list:
    """List of lambda functions with argument: project name. Some will execute a request.
    The functions will return a tuple of (file_name, file_text)"""
    return [
        lambda x: (".projectile", ""),
        lambda x: ("README.md", f"# {x}"),
        lambda x: (".python-version", "3.7.13"),
        lambda x: ("LICENSE", requests.get(LICENSE).text),
        lambda x: ("Makefile", get_makefile(x)),
        lambda x: (".gitignore", requests.get(GITIGNORE).text),
    ]


def get_src_files() -> list:
    """List of lambda functions with argument: project name, author name."""
    return [
        lambda p, a: (
            f"{p}.org",
            (
                f"#+title: {p}\n#+subtitle: \n#+author: {a}\n"
                "#+SETUPFILE: ../config/org-theme.config\n"
                "#+SETUPFILE: ../config/org-header.config\n"
                f"\n* {p}"
            ),
        ),
    ]


def get_submodules() -> list:
    """List of lambda functions with argument: project name.
    They will return a tuple of (ssh git path, local Path object)."""
    return [
        lambda x: (
            SM_CONFIG,
            "config",
        ),
        lambda x: (
            SM_THEME,
            directories.resources / "theme",
        ),
    ]
