import os


def run_compile(filename, debug):
    from .module import DenModule

    if os.path.isfile(filename):
        with open(filename, "r") as f:
            text = f.read()
    else:
        print(
            f"{Color.RED}ERROR{Color.RESET}: No such file {Color.BLUE}{os.path.abspath(filename)}{Color.RESET}"
        )
        quit()

    text = " " + text
    return DenModule(
        os.path.basename(filename), os.path.abspath(filename), text=text, debug=debug
    )
