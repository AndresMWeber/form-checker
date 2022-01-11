import os
import re
import logging
from cv2 import (
    CAP_PROP_FPS,
    CAP_PROP_POS_FRAMES,
    CAP_PROP_FRAME_COUNT,
    VideoCapture,
    VideoWriter_fourcc,
    VideoWriter,
)
from pathlib import Path, PurePath

from form_checker.utils.filename import get_basename_with_suffix, is_url


class Video:
    def __init__(self, file_path):

        if not (Path(file_path).is_file() or is_url(file_path)):
            raise FileNotFoundError(
                f"The specified video is not a valid url or file path: {file_path}"
            )

        self.vidcap = VideoCapture(file_path)
        self.width = int(self.vidcap.get(3))
        self.height = int(self.vidcap.get(4))
        self.p = PurePath(file_path)
        self.fps = self.vidcap.get(CAP_PROP_FPS)

    def set_desired_frames(self):
        self.frame_step = 1
        return self

    def get_frame(self, frame):
        self.vidcap.set(CAP_PROP_POS_FRAMES, frame)
        success, image = self.vidcap.read()
        return image if success else []

    def release(self):
        self.vidcap.release()

    def write(self, img):
        self.output.write(img)

    def __len__(self):
        return int(self.vidcap.get(CAP_PROP_FRAME_COUNT))

    def __call__(self, filename):
        self.output_filename = f'/tmp/{re.match(r"([\w.]+)(?:\?)", filename)[1]}'
        self.compressed_filename = get_basename_with_suffix(
            self.output_filename, "compressed"
        )
        return self

    def __enter__(self):
        logging.info(
            f"Writing out file: {self.output_filename} - {self.width} x {self.height}"
        )
        mp4_fourcc = VideoWriter_fourcc(*"mp4v")
        self.output = VideoWriter(
            self.output_filename,
            fourcc=mp4_fourcc,
            fps=self.fps / 4,
            frameSize=(self.width, self.height),
        )
        return self

    def __exit__(self, *args, **kwargs):
        self.release()
        self.output.release()
        try:
            logging.info(
                f"ffmpeg -y -i {self.output_filename} -vcodec libx264 {self.compressed_filename}"
            )
            os.system(
                f"ffmpeg -y -i '{self.output_filename}' -vcodec libx264 '{self.compressed_filename}'"
            )
        except Exception as e:
            logging.error(f"Failed creating compressed version: {e.message}")
