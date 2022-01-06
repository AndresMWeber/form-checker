import os
import logging
import cv2
from pathlib import Path, PurePath

from form_checker.utils.filename import get_basename_with_suffix


class Video:
    def __init__(self, file_path):

        if not (Path(file_path).is_file()):
            raise FileNotFoundError(
                f"Could not find associated video file {file_path}"
            )

        self.vidcap = cv2.VideoCapture(file_path)
        self.width = int(self.vidcap.get(3))
        self.height = int(self.vidcap.get(4))
        self.p = PurePath(file_path)
        self.fps = self.vidcap.get(cv2.CAP_PROP_FPS)

    def set_desired_frames(self):
        self.frame_step = 1
        return self

    def get_frame(self, frame):
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = self.vidcap.read()
        return image if success else []

    def release(self):
        self.vidcap.release()

    def write(self, img):
        self.output.write(img)

    def __len__(self):
        return int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __call__(self, filename):
        self.output_filename = filename
        return self

    def __enter__(self):
        logging.info(
            f"Writing out file: {self.output_filename} - {self.width} x {self.height}"
        )
        mp4_fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.output = cv2.VideoWriter(
            self.output_filename,
            fourcc=mp4_fourcc,
            fps=self.fps / 4,
            frameSize=(self.width, self.height),
        )
        return self

    def __exit__(self, *args, **kwargs):
        self.release()
        self.output.release()
        cv2.destroyAllWindows()
        try:
            logging.info(
                f"ffmpeg -i {self.output_filename} -vcodec libx264 {get_basename_with_suffix(self.output_filename, 'compressed')}"
            )
            os.system(
                f"ffmpeg -i '{self.output_filename}' -vcodec libx264 '{get_basename_with_suffix(self.output_filename, 'compressed')}'"
            )
        except Exception as e:
            logging.error(f"Failed creating compressed version: {e.message}")
