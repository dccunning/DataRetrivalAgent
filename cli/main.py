import argparse
import subprocess
import os


def launch_ui(args):
    if args.manifest:
        os.environ["DRA_MANIFEST_PATH"] = args.manifest
    if args.catalog:
        os.environ["DRA_CATALOG_PATH"] = args.catalog

    subprocess.run(["streamlit", "run", "ui/local_mode.py"])


def main():
    parser = argparse.ArgumentParser(prog="dra")
    subparsers = parser.add_subparsers(dest="command")

    run_cmd = subparsers.add_parser("run", help="Launch the DRA UI")
    run_cmd.add_argument("--manifest", help="Path to manifest.json")
    run_cmd.add_argument("--catalog", help="Path to catalog.json")

    args = parser.parse_args()

    if args.command == "run":
        launch_ui(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
