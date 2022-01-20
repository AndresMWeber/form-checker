import re
from pathlib import Path
from form_checker.settings import Config


url_regex = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)",
    re.IGNORECASE,
)


def get_basename_with_suffix(path: str, suffix: str) -> str:
    p = Path(path)
    if p.is_dir():
        raise IOError("Must provide a file path, not a directory.")
    return p.name.replace(p.suffix, f"_{suffix}{p.suffix}")


def is_url(candidate: str) -> bool:
    return re.match(url_regex, candidate) is not None


def strip_querystring(url: str) -> str:
    return re.match(r"([\_\-\/:\.\w.]+)\??", url)[1]


def prepend_tmp_dir(secondary_path: str) -> str:
    return str(Path(Config.TEMP_DIR) / secondary_path)
