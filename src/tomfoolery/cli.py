import argparse
import ast_comments as ast

from pathier import Pathier, Pathish

from tomfoolery import TomFoolery


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
    args = parser.parse_args()
    return args


def generate_from_file(datapath: Pathish, outpath: Pathish | None = None):
    """Generate a `dataclass` named after the file `datapath` points at.

    If `outpath` is not given, the output file will be the same as `datapath`, but with a `.py` extension.

    Can be any `.toml` or `.json` file where all keys are valid Python variable names."""

    datapath = Pathier(datapath)
    if outpath:
        outpath = Pathier(outpath)
    else:
        outpath = datapath.with_suffix(".py")
    module = ast.parse(outpath.read_text()) if outpath.exists() else None
    data = datapath.loads()
    fool = TomFoolery(module)  # type: ignore
    source = fool.generate(datapath.stem, data)
    source = fool.format_str(source.replace("filepath", datapath.name))
    outpath.write_text(source)


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    generate_from_file(args.file, args.outpath)


if __name__ == "__main__":
    main(get_args())
