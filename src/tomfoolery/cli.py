import argparse

import tomfoolery


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file",
        type=str,
        help=""" The file to generate dataclasses from. Can be a .toml or .json file, but all keys must be valid Python variable names. 
        The generated dataclasses will be written to a file of the same name, but with a `.py` extension.""",
    )

    parser.add_argument(
        "-o",
        "--outpath",
        type=str,
        default=None,
        help=""" The output file path. If not given, the output will be named after the `file` arg, but with a `.py` extension. """,
    )
    parser.add_argument(
        "-nr",
        "--no_recursion",
        action="store_false",
        help=""" Don't recursively create dataclasses for values that are dictionaries.""",
    )
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    tomfoolery.generate_from_file(args.file, args.outpath, args.no_recursion)


if __name__ == "__main__":
    main(get_args())
