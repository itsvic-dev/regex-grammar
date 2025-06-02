import sys
import logging
import argparse

from . import parse_file, syntax as s


# keeps the scope clean
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show detailed debug information"
    )
    return parser.parse_args()


def main_cli():
    args = get_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    filename = args.filename
    if filename == "-":
        filename = "<stdin>"
        file = sys.stdin
    else:
        file = open(filename)
    tree = parse_file(file)
    file.close()

    # grab the first def (the 'start') and to_regex() it
    # we get its superclass first so that we dont get the extra group around it
    start = tree[0]
    print(super(s.GroupDef, start).to_regex())
