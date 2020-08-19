import argparse
from pathlib import Path
from typing import Optional
from rsi import (
    export_web_dmi_to_rsi,
    Rsi,
    HyphenSplitter,
    NumberSplitter,
    SimpleSplitter,
    UnderscoreSplitter,
)


def main() -> int:
    """
    Entry point for the command line rsi utility script.
    """
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    _from_dmi = subparser.add_parser("from_dmi", help="Will create an RSI from a BYOND DMI file.")
    _from_dmi.add_argument("input", help="The DMI file to read from.", type=Path)
    _from_dmi.add_argument("output", help="The RSI to output to.", type=Path)
    _from_dmi.add_argument("-c", "--copyright", help="Specifies the copyright of the new RSI file.")
    _from_dmi.add_argument("-l", "--license", help="Specifies the license of the new RSI file.")

    _new_rsi = subparser.add_parser("new", help="Will create a new RSI at the provided directory.")
    _new_rsi.add_argument("rsi", help="The location of the new RSI. Must not exist yet.", type=Path)
    _new_rsi.add_argument("dimensions", help="The dimensions of the new rsi, in <width>x<height> format, like so: 32x32.")
    _new_rsi.add_argument("-c", "--copyright", action="store", help="Copyright info for this RSI file such as author.", nargs="?")
    _new_rsi.add_argument("-l", "--license", action="store", help="The license of this RSI file, as valid SPDX License Identifier (Google it).", nargs="?")
    _new_rsi.add_argument("--dont-make-parent-dirs", action="store_true", help="Do not create parent directories if they do not exist, instead throw an error.", dest="no_parents")

    _web_rsi = subparser.add_parser("web", help="Download a .dmi and convert to an .rsi")
    _web_rsi.add_argument("url", help="Web url of the blob holding the .dmi")
    _web_rsi.add_argument("output", help="Specifies the output file name.")
    _web_rsi.add_argument("-l", "--license", action="store", help="The license of this RSI file, as valid SPDX License Identifier (Google it).", nargs="?")
    _web_rsi.add_argument("-s", "--splitter", action="store", help="The class to split the rsi states if required.")
    _web_rsi.add_argument("-i", "--indents", action="store", help="The number of indents for meta.json")

    args = parser.parse_args()

    if args.command == "from_dmi":
        from_dmi(args.input, args.output, args.license, args.copyright)
        return 0

    if args.command == "new":
        return new_rsi(args.rsi, args.dimensions, args.copyright, args.license, not args.no_parents)

    if args.command == "web":
        if isinstance(args.indents, str):
            args.indents = int(args.indents)

        return web_rsi(args.url, args.output, args.license, args.splitter, args.indents)

    print("No command specified!")
    return 1


def from_dmi(inputf: Path, output: Path, new_license: Optional[str], new_copyright: Optional[str]) -> None:
    rsi = Rsi.from_dmi(inputf)
    if new_license:
        rsi.license = new_license
    if new_copyright:
        rsi.copyright = new_copyright
    rsi.write(output)


def new_rsi(loc: Path,
            dimensions: str,
            rsi_copyright: Optional[str],
            rsi_license: Optional[str],
            make_parents: bool) -> int:
    try:
        dimsplit = dimensions.split("x")
        if len(dimsplit) != 2:
            print("Incorrect amount of dimensions passed, expected exactly 2.")
            return 1
        x = int(dimsplit[0])
        y = int(dimsplit[1])

    except ValueError:
        print("Invalid dimensions passed.")
        return 1

    if not loc.parent.exists() and not make_parents:
        print("Parent directories do not exist. Aborting.")
        return 1

    rsi = Rsi((x, y))
    rsi.license = rsi_license
    rsi.copyright = rsi_copyright
    rsi.write(loc, make_parents)

    return 0


def web_rsi(url: str,
            output: Path,
            rsi_license: Optional[str] = "",
            splitter: Optional[str] = "",
            indents: Optional[int] = None) -> int:

    splitter_class = {
        "hyphen": HyphenSplitter,
        "number": NumberSplitter,
        "simple": SimpleSplitter,
        "underscore": UnderscoreSplitter,
    }.get(splitter, None)

    if splitter is not None and splitter_class is None:
        print(f"Invalid splitter supplied")
        return 1

    output = Path(output)

    export_web_dmi_to_rsi(url, output, rsi_license, splitter_class, indents)
    return 0
