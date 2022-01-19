import logging
import argparse
from pathlib import Path

from form_checker.main import process
from form_checker.utils.aws import get_presigned_url, upload_file
from form_checker.utils.general import add_bucket_prefix

try:
    import tkinter
    from tkinter.filedialog import askopenfilename
except:
    logging.warning("Failed to load tkinter. UI invocation unavailable.")


def run(file_path=None, key=None, bucket=None, upload=False):
    if not file_path:
        if not (key and bucket):
            raise IOError(
                "You must supply file_path or key/bucket to continue."
            )
        else:
            file_path = get_presigned_url(bucket, key)

    processed_file = process(file_path)

    if upload and bucket:
        destination_key = add_bucket_prefix(
            key or Path(processed_file).name, "processed"
        )
        logging.info(
            f"Uploading file {processed_file} to {bucket}/{destination_key}"
        )
        upload_file(
            processed_file,
            bucket,
            destination_key,
        )

    logging.info("Finished processing video successfully.")


def ui():
    root = tkinter.Tk()
    root.wm_withdraw()
    filename = askopenfilename()
    run(file_path=filename)


def cli():
    # All the logic of argparse goes in this function
    parser = argparse.ArgumentParser(
        description="Generate a pose overlay on specified video."
    )
    parser.add_argument(
        "target", type=str, help="the path of the local video file"
    )
    parser.add_argument(
        "-u",
        "--upload",
        dest="upload",
        action="store_true",
        help="Upload to s3 or not.",
    )
    parser.add_argument(
        "-b",
        "--bucket",
        dest="bucket",
        default=None,
        help="Which S3 bucket to use.",
    )
    parser.add_argument(
        "-k",
        "--key",
        dest="key",
        default=None,
        help="Where to find the original file.",
    )

    args = parser.parse_args()

    required_together = ("upload", "bucket")

    if not all([getattr(args, x) for x in required_together]):
        raise RuntimeError(
            "If using key upload, you must supply --bucket, -b as well."
        )

    if not args.target:
        logging.error("Must specify a file.")
        raise TypeError(
            "You must specify a file as the first positional argument"
        )

    run(
        file_path=args.target,
        key=args.key,
        bucket=args.bucket,
        upload=args.upload,
    )
