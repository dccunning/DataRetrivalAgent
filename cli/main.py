import argparse
import subprocess


def launch_ui():
    subprocess.run(["streamlit", "run", "ui/local_mode.py"])


def main():
    """
    CLI entry point: `dra run`
    """
    parser = argparse.ArgumentParser(prog="dra")
    subparsers = parser.add_subparsers(dest="command")

    run_cmd = subparsers.add_parser("run", help="Launch the DRA UI")

    args = parser.parse_args()

    if args.command == "run":
        launch_ui()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
