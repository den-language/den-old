import argparse
import os.path as path

from codegen import DenModule
from helpers.color import init_color, Color
from helpers.llvm_gen import initialize
from codegen.generate_module import run_compile


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A compiled programming language that is designed to be fast, simple, and modern.",
        prefix_chars="-+/",
    )

    parser.add_argument("filename", type=str, help="A required input file")

    parser.add_argument(
        "output",
        type=str,
        nargs="?",
        help="Optional output folder (defaults to `./build/`)",
    )

    parser.add_argument("-d", "--debug", action="store_true", help="Turn on debug mode")

    args = parser.parse_args()

    init_color()
    initialize()

    module = run_compile(args.filename, args.debug)
    module.generate()
    module.write(folder=args.output)

    print(f"{Color.BOLD}{Color.BLUE}All Done!{Color.RESET} 🎉")
