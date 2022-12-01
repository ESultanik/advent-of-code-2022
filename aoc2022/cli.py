import argparse
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile

from . import CHALLENGES


def main(argv: [str]) -> int:
    parser = argparse.ArgumentParser(description="Evan Sultanik's Advent of Code Solutions")

    parser.add_argument("INPUT", type=Path, nargs="?", default=Path("-"),
                        help="path to the input file (default is STDIN)")
    challenge_group = parser.add_mutually_exclusive_group(required=True)
    challenge_group.add_argument("--day", "-d", type=int, choices=sorted(CHALLENGES.keys()), help="the day number")
    challenge_group.add_argument("--list", "-l", action="store_true", help="list all available challenges")
    parser.add_argument("--part", "-p", type=int, default=-1, help="the part of the challenge to run; if the part is "
                                                                   "negative, then all parts for the given day will be "
                                                                   "run (default=-1)")
    parser.add_argument("--output", "-o", type=str, help="path to the output file, or '-' for STDOUT (the default)",
                        default="-")

    args = parser.parse_args()

    if hasattr(args, "list") and args.list:
        for day, parts in sorted(CHALLENGES.items()):
            if not parts:
                continue
            print(f"Day {day}:")
            for i, part in parts.items():
                print(f"\tPart {i}:\t{part.__name__}")
        return 0

    if args.day not in CHALLENGES:
        sys.stderr.write(f"Unknown day: {args.day}\n")
        return 1

    if args.part < 0:
        parts = sorted(CHALLENGES[args.day].items())
    elif args.part not in CHALLENGES[args.day]:
        sys.stderr.write(f"Day {args.day} does not have part {args.part}\n")
        return 1
    else:
        parts = [(args.part, CHALLENGES[args.day][args.part])]

    delete_on_exit = False
    if args.INPUT.name == "-":
        tmpfile = NamedTemporaryFile("w", delete=False)
        tmpfile.write(sys.stdin.read())
        tmpfile.close()
        infile = Path(tmpfile.name)
        delete_on_exit = True
    else:
        infile = args.INPUT

    if args.output == "-":
        outfile = sys.stdout
    else:
        outfile = open(args.output, "w")

    try:
        if sys.stderr.isatty() and outfile.isatty():
            sys.stderr.write(f"Day {args.day}\n")
        for part, func in parts:
            if sys.stderr.isatty() and outfile.isatty():
                sys.stderr.write(f"Running {func.__name__}...\n")
            result = func(infile)
            if sys.stderr.isatty() and outfile.isatty():
                sys.stderr.write(f"Part {part}: ")
                sys.stderr.flush()
            outfile.write(f"{result!s}\n")
            outfile.flush()

    finally:
        if delete_on_exit:
            infile.unlink()
        if outfile != sys.stdout:
            outfile.close()
