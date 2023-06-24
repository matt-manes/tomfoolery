import argparse

from pathier import Pathier

from tomfoolery import TomFoolery


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file",
        type=str,
        help=""" The file to generate dataclasses from. Can be a .toml or .json file, but all keys must be valid Python variable names. 
        The generated dataclasses will be written to a file of the same name, but with a `.py` extension.""",
    )
    args = parser.parse_args()

    return args


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    fool = TomFoolery()
    fool.generate_from_file(args.file, True)


if __name__ == "__main__":
    main(get_args())
