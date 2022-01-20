import os
from pathlib import Path


class Config:
    BUCKET = os.getenv("UPLOAD_BUCKET", "form-checker-videos")
    COMPRESS_OUTPUT = os.getenv("FC_COMPRESS_OUTPUT", True)
    FPS_SPEED_MULTIPLIER = os.getenv("FC_RETIME_MULTIPLIER", 0.25)
    RETIME_OUTPUT = os.getenv("FC_RETIME_OUTPUT", False)
    OUTPUT_CODEC = os.getenv("FC_OUTPUT_CODEC", "mp4v")
    V_CODEC = os.getenv("FC_V_CODEC", "libx264")
    TEMP_DIR = (
        "/tmp"
        if os.getenv("AWS_LAMBDA_FUNCTION_NAME")
        else Path("./tmp").resolve()
    )
    KEY_SUFFIX = os.getenv("FC_KEY_SUFFIX", "processed")
    PROCESSED_FILE_SUFFIX = os.getenv("FC_OUTPUT_SUFFIX", "processed")
    COMPRESSED_FILE_SUFFIX = os.getenv(
        "FC_COMPRESSED_OUTPUT_SUFFIX", "compressed"
    )


def class_to_str(cls):
    return "\n".join(
        "%s: %s" % item
        for item in cls.__dict__.items()
        if not item[0].startswith("__")
    )
