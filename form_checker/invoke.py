import logging
import argparse
from form_checker.main import process

try:
    import tkinter
    from tkinter.filedialog import askopenfilename
except:
    logging.warning("Failed to load tkinter. UI invocation unavailable.")


def ui():

    root = tkinter.Tk()
    root.wm_withdraw()
    filename = askopenfilename()
    process(filename, True)


def cli():
    # All the logic of argparse goes in this function
    parser = argparse.ArgumentParser(
        description="Generate a pose overlay on specified video."
    )
    parser.add_argument(
        "target", type=str, help="the path of the local video file"
    )
    parser.add_argument(
        "--end",
        dest="end",
        default="!",
        help="sum the integers (default: find the max)",
    )

    args = parser.parse_args()
    process(args.target, end=args.end)
