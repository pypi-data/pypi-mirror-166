"""
Parse arguments and generate all files from local and remote sources.
Use "sources" and "install" files for configuration and functions.
"""
import argparse

from . import sources
from . import install


def main(argc: int, argv: argparse.Namespace):
    author = argv.author
    project = argv.project
    install.is_empty_cwd()
    install.git_init()
    for directory in sources.directories:
        try:
            install.build_dir(directory)
        except Exception as e:
            print(f"Could not build directory: {directory}\n", e)

    for file in sources.get_root_files():
        try:
            install.build_file(*file(project))
        except Exception as e:
            print(f"Could not build file: {file}\n", e)

    for file in sources.get_src_files():
        try:
            install.build_file(*file(project, author), sources.directories.src)
        except Exception as e:
            print(f"Could not build file: {file}\n", e)

    for submodule in sources.get_submodules():
        try:
            install.install_dependency(*submodule(project))
        except Exception as e:
            print(f"Could not install submodule: {submodule}\n", e)

    print("\033[1mAll set. Ready to go!\x1b[0m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install org-template.")
    parser.add_argument(
        "project",
        metavar="project name",
        type=str,
        help="Name for the project.",
    )
    parser.add_argument(
        "-a",
        "--author",
        metavar="author name",
        type=str,
        help="Name of the author.",
        default="",
    )
    args = parser.parse_args()
    main(len(args.__dict__), args)
