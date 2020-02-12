import argparse
import os.path as path

from module import DenModule
from helpers.color import init_color
from helpers.llvm_gen import initialize


def run_compile(args):
    if path.isfile(args.filename):
        with open(args.filename, "r") as f:
            text = f.read()
    else:
        print(f"ERROR: No such file {args.filename}")
        quit()
    
    text = " " + text
    module = DenModule(path.basename(args.filename), text=text, debug=args.debug)
    module.generate(folder=args.output)


parser = argparse.ArgumentParser(
    description="A compiled programming language that is designed to be fast, simple, and modern.",
    prefix_chars="-+/"
)

parser.add_argument("filename", type=str,
                    help="A required input file")

parser.add_argument("output", type=str, nargs="?",
                    help="Optional output folder (defaults to filename)")

parser.add_argument("-d", "--debug", action="store_true",
                    help="Turn on debug mode")


args = parser.parse_args()

init_color()
initialize()

run_compile(args)
