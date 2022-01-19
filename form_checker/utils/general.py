import os
import re
import sys
import threading
from toml import load as toml_load


project_data = toml_load("pyproject.toml")


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


def get_project_attribute(*paths):
    data = project_data
    for path in paths:
        data = data[path]
    return data


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)"
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()


def add_bucket_prefix(key: str, target: str) -> str:
    corrected = re.sub(r"$(\w+)(?=\/)", target, key, 1)
    if corrected == key:
        return f"processed/{key}"
    return corrected
