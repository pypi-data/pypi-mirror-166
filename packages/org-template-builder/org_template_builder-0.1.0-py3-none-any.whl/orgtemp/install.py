"""
Functions that call subprocesses or create paths.
This will execute git commands to initialize and install submodules.
"""
import subprocess
from pathlib import Path


def is_empty_cwd() -> bool:
    """Check if the current directory is empty or not.
    Raise ValueError if it is not empty."""
    path = Path.cwd()
    listdir = list(path.glob("[!.]*"))  # check for non-hidden files
    if len(listdir) > 0:
        raise ValueError("Directory is not empty!")
    return True


def git_init():
    """Check for git directory in path, if it doesn't exists, create it."""
    path = Path.cwd()
    git: Path = path / ".git"
    if not git.is_dir():
        subprocess.call(["git", "init"])
        # Use main branch instead of master
        subprocess.call(["git", "checkout", "-b", "main"])


def build_dir(directory: Path, root: Path = Path.cwd()) -> Path:
    """Create given path directory, skip if exists."""
    if not directory.is_dir():
        Path.mkdir(root / directory)
        print(f"Built directory: {root / directory}")
        return directory
    print(f"Directory '{directory}' already exists.")
    return directory


def build_file(name: str, data: str = "", path: Path = Path.cwd()) -> Path:
    """Create file by name, use path argument to extend its parents.
    Use data string for the content written to the file."""
    f = path / Path(name)
    subprocess.call(["touch", f])
    if not f.is_file():
        print(f"Could not create file {name}")
    with open(f, "w") as file:
        file.write(data)
    print(f"Created {name}")
    return f


def install_dependency(url: str, path: str):
    """Git submodule add url to given path."""
    subprocess.call(["git", "submodule", "add", url, path])
    print(f"Installed {path}")
