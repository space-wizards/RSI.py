#!/usr/bin/env python3

import argparse
from pathlib import Path
from rsi import Rsi
from typing import Optional


def main() -> None:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    _from_dmi = subparser.add_parser("from_dmi", help="Will create an RSI from a BYOND DMI file.")
    _from_dmi.add_argument("input", help="The DMI file to read from.", type=Path)
    _from_dmi.add_argument("output", help="The RSI to output to.", type=Path)
    _from_dmi.add_argument("--license", help="Specifies the license of the new RSI file.")
    _from_dmi.add_argument("--copyright", help="Specifies the copyright of the new RSI file.")

    args = parser.parse_args()

    if args.command == "from_dmi":
        from_dmi(args.input, args.output, args.license, args.copyright)
        return

    print("No command specified!")


def from_dmi(inputf: Path, output: Path, new_license: Optional[str], new_copyright: Optional[str]) -> None:
    rsi = Rsi.from_dmi(inputf)
    if new_license:
        rsi.license = new_license
    if new_copyright:
        rsi.copyright = new_copyright
    rsi.write(output)


if __name__ == "__main__":
    main()
