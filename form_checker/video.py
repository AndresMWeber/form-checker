import os
import logging
from cv2 import (
    CAP_PROP_FPS,
    CAP_PROP_POS_FRAMES,
    CAP_PROP_FRAME_COUNT,
    CAP_PROP_FOURCC,
    VideoCapture,
    VideoWriter_fourcc,
    VideoWriter,
)
from pathlib import Path, PurePath

from form_checker.utils.filename import (
    get_basename_with_suffix,
    is_url,
    strip_querystring,
)


class Video:
    def __init__(self, file_path):
        path = Path(file_path)
        if not (path.is_file() or is_url(file_path)):
            raise FileNotFoundError(
                f"The specified video is not a valid url or file path: {file_path}"
            )

        if not is_url(file_path):
            file_path = str(path.resolve())

        self.vidcap = VideoCapture(file_path)
        logging.info(f"Loaded state of video: {self.vidcap.isOpened()}")
        self.width = int(self.vidcap.get(3))
        self.height = int(self.vidcap.get(4))
        self.fps = self.vidcap.get(CAP_PROP_FPS)
        self.p = PurePath(file_path)

        self.fps_multiplier = 0.25
        self.temp_dir = (
            "/tmp"
            if os.getenv("AWS_LAMBDA_FUNCTION_NAME")
            else Path("./tmp").resolve()
        )
        self.input_codec = self.get_input_codec()
        self.output_codec = "mp4v"
        self.v_codec = "libx264"
        logging.info(
            f"Received file {self.p}: {self.width}x{self.height}@{self.fps} - {len(self)} frames - {self.input_codec}"
        )

    def get_input_codec(self):
        h = int(self.vidcap.get(CAP_PROP_FOURCC))
        return (
            chr(h & 0xFF)
            + chr((h >> 8) & 0xFF)
            + chr((h >> 16) & 0xFF)
            + chr((h >> 24) & 0xFF)
        )

    def set_desired_frames(self):
        self.frame_step = 1
        return self

    def get_frame(self, frame):
        self.vidcap.set(CAP_PROP_POS_FRAMES, frame)
        success, image = self.vidcap.read()
        if not success:
            logging.error(f"Failed getting frame {frame}")
        return image if success else []

    def release(self):
        self.vidcap.release()

    def write(self, img):
        self.output.write(img)

    def __len__(self):
        return int(self.vidcap.get(CAP_PROP_FRAME_COUNT))

    def __call__(self, filename):
        # Cut off any extra query strings from a possible URL file name and prepend the temp dir.
        base_name = strip_querystring(filename)
        self.output_filename = os.path.join(self.temp_dir, base_name)
        self.compressed_filename = os.path.join(
            self.temp_dir,
            get_basename_with_suffix(self.output_filename, "compressed"),
        )
        try:
            os.mkdir(self.temp_dir)
        except OSError:
            logging.debug(
                f"Temp dir already exists, skipping creation...{self.temp_dir}"
            )
        return self

    def __enter__(self):
        logging.info(
            f"Output filename will be: {self.output_filename} - {self.width} x {self.height}"
        )
        self.output = VideoWriter(
            self.output_filename,
            fourcc=VideoWriter_fourcc(*self.output_codec),
            fps=self.fps * self.fps_multiplier,
            frameSize=(self.width, self.height),
        )
        return self

    def __exit__(self, *args, **kwargs):
        if args[0] == OSError:
            return
        self.release()
        self.output.release()
        command = f"ffmpeg -y -i '{self.output_filename}' -vcodec {self.v_codec} '{self.compressed_filename}'"
        try:
            logging.info(command)
            os.system(command)
        except Exception as e:
            logging.error(f"Failed creating compressed version: {e.message}")
