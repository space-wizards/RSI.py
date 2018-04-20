#!/usr/bin/env python3

import argparse
from pathlib import Path
from rsi import Rsi


def main() -> None:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    _from_dmi = subparser.add_parser("from_dmi", help="Will create an RSI from a BYOND DMI file.")
    _from_dmi.add_argument("input", help="The DMI file to read from.", type=Path)
    _from_dmi.add_argument("output", help="The RSI to output to.", type=Path)

    args = parser.parse_args()

    if args.command == "from_dmi":
        from_dmi(args.input, args.output)
        return

    print("No command specified!")


def from_dmi(inputf: Path, output: Path) -> None:
    rsi = Rsi.from_dmi(inputf)
    rsi.write(output)


if __name__ == "__main__":
    main()
