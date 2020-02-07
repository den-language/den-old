import subprocess
import os.path as path

subprocess.run(
    f"python3.8 {path.abspath(path.join(path.dirname(__file__), '../den'))}",
    shell=True,
    check=True,
)
