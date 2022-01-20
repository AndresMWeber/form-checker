from pathlib import Path
from unittest import TestCase
from form_checker.utils.general import (
    add_bucket_prefix,
    get_project_attribute,
    ProgressPercentage,
)

from unittest import mock


class TestAddBucketPrefix(TestCase):
    def test_home_dir(self):
        assert add_bucket_prefix(
            str(Path.home() / "test.mp4"), "folder"
        ).startswith("folder/")

    def test_s3(self):
        assert (
            add_bucket_prefix(r"test/produce/Finance/test.mp4", "folder")
            == r"folder/produce/Finance/test.mp4"
        )

    def test_only_filename(self):
        assert add_bucket_prefix(r"test.mp4", "folder") == r"folder/test.mp4"

    def test_bad_path(self):
        assert (
            add_bucket_prefix(r"\\test/produce/Finance/test.mp4", "folder")
            == r"\\folder/produce/Finance/test.mp4"
        )


class TestProgressPercentage(TestCase):
    def test_default(self):
        with mock.patch("os.path.getsize", return_value=2 * 1024 * 1024):
            p = ProgressPercentage(str(Path.home() / "test.mp4"))
            assert p._size == 2 * 1024 * 1024
            p(400)
            assert p._seen_so_far == 400


class TestGetProjectAttribute(TestCase):
    def test_default(self):
        assert get_project_attribute("tool", "poetry", "name") == "form_checker"
