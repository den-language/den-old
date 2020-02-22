import argparse
import subprocess  # For linking object files (don't scream at me)

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
        help="Optional output executable (defaults to `./build/a.out`)",
    )

    parser.add_argument("-d", "--debug", action="store_true", help="Turn on debug mode")
    parser.add_argument("-o", "--object", action="store_true", help="Don't link files")

    args = parser.parse_args()

    init_color()
    initialize()

    module = run_compile(args.filename, args.debug, args.output)
    module.generate()
    module.write()

    if args.object is not None:
        try:
            subprocess.check_output(
                ["clang", "-fdiagnostics-color", "-o", module.output_file]
                + module.to_link,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as err:
            print(err.output.decode("utf-8"), end="")
            quit(1)

    print(f"{Color.BOLD}{Color.BLUE}All Done!{Color.RESET} 🎉")
