import re
from pathlib import PurePath


url_regex = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)",
    re.IGNORECASE,
)


def get_basename_with_suffix(path, suffix):
    p = PurePath(path)
    return p.name.replace(p.suffix, f"_{suffix}{p.suffix}")


def is_url(candidate: str) -> bool:
    return re.match(url_regex, candidate) is not None


def strip_querystring(url: str) -> str:
    return re.match(r"([\_\-\/:\.\w.]+)\??", url)[1]
