import subprocess
import sys


def main():
    commands = [
        [sys.executable, "-m", "ruff", "check", "."],
        [sys.executable, "-m", "ruff", "format", "--check", "."],
        [sys.executable, "-m", "pytest"],
    ]

    for command in commands:
        subprocess.run(command, check=True)

    print("All quality checks passed.")


if __name__ == "__main__":
    main()
