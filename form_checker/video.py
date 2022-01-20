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
from form_checker.settings import Config

from form_checker.utils.filename import (
    get_basename_with_suffix,
    is_url,
    strip_querystring,
    prepend_tmp_dir,
)


class Video:
    def __init__(self, file_path: str):
        self.output = None
        self._raw_filepath = file_path
        self._validate_path()
        self.vidcap = VideoCapture(self.local_filepath)
        logging.info(
            f"Loaded state of video: {self.vidcap.isOpened()} from {self.local_filepath}"
        )
        logging.info(
            f"Computed File Paths:\nraw - {self._raw_filepath}\nlocal - {self.local_filepath}\nfilename - {self.local_filename}\ncompressed - {self.compressed_filename}\nuncompressed - {self.uncompressed_filename}"
        )

        # Get video information
        self.input_codec = self.get_input_codec()
        self.width = int(self.vidcap.get(3))
        self.height = int(self.vidcap.get(4))
        cv2_fps = self.vidcap.get(CAP_PROP_FPS)
        self.fps = cv2_fps if cv2_fps > 20 else 24
        logging.info(
            f"Received file {self._raw_filepath}: {self.width}x{self.height}@{self.fps} - {len(self)} frames - {self.input_codec}"
        )

    def _validate_path(self):
        self.from_url = is_url(self._raw_filepath)
        if not (Path(self._raw_filepath).is_file() or self.from_url):
            raise FileNotFoundError(
                f"The specified video is not a valid url or file path: {self._raw_filepath}"
            )
        self.path = Path(self._raw_filepath)

    def get_input_codec(self):
        h = int(self.vidcap.get(CAP_PROP_FOURCC))
        return (
            chr(h & 0xFF)
            + chr((h >> 8) & 0xFF)
            + chr((h >> 16) & 0xFF)
            + chr((h >> 24) & 0xFF)
        )

    def get_frame(self, frame):
        logging.info(f"Processing frame {frame}/{len(self)}")
        self.vidcap.set(CAP_PROP_POS_FRAMES, frame)
        success, image = self.vidcap.read()
        if not success:
            logging.error(f"Failed getting frame {frame}")
        return image if success else []

    def release(self):
        self.vidcap.release()
        if self.output:
            self.output.release()

    def write(self, img):
        if self.output:
            self.output.write(img)

    def _generate_filename(self, suffix: str) -> str:
        return prepend_tmp_dir(
            get_basename_with_suffix(
                self.local_filename,
                suffix,
            )
        )

    @property
    def local_filepath(self):
        return self._raw_filepath if self.from_url else str(self.path.resolve())

    @property
    def local_filename(self):
        return strip_querystring(self.path.name)

    @property
    def output_filename(self):
        return (
            self.compressed_filename
            if Config.COMPRESS_OUTPUT
            else self.uncompressed_filename
        )

    @property
    def uncompressed_filename(self):
        return self._generate_filename(Config.PROCESSED_FILE_SUFFIX)

    @property
    def compressed_filename(self):
        return self._generate_filename(Config.COMPRESSED_FILE_SUFFIX)

    @property
    def _ffmpeg_cmd(self):
        return f"ffmpeg -y -i '{self.uncompressed_filename}' -vcodec {Config.V_CODEC} '{self.compressed_filename}'"

    def __len__(self):
        return int(self.vidcap.get(CAP_PROP_FRAME_COUNT))

    def __enter__(self):
        try:
            os.mkdir(Config.TEMP_DIR)
        except OSError:
            logging.debug(
                f"Temp dir already exists, skipping creation...{Config.TEMP_DIR}"
            )
        logging.info(
            f"Output filename will be: {self.output_filename} - {self.width} x {self.height}"
        )
        self.output = VideoWriter(
            self.uncompressed_filename,
            fourcc=VideoWriter_fourcc(*Config.OUTPUT_CODEC),
            fps=self.fps
            * (Config.FPS_SPEED_MULTIPLIER if Config.RETIME_OUTPUT else 1),
            frameSize=(self.width, self.height),
        )
        return self

    def __exit__(self, *args, **kwargs):
        if args[0] == OSError:
            return
        self.release()
        if Config.COMPRESS_OUTPUT:
            try:
                logging.info(self._ffmpeg_cmd)
                os.system(self._ffmpeg_cmd)
            except Exception as e:
                _, message = e.args
                logging.error(f"Failed creating compressed version: {message}")
