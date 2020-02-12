import subprocess
import os.path as path


def test_main():
    subprocess.run(
        [
            "python3.8",
            f"{path.abspath(path.join(path.dirname(__file__), '../den'))}",
            f"{path.abspath(path.join(path.dirname(__file__), '../examples'))}/functions.py",
        ],
        shell=True,
        check=True,
    )
