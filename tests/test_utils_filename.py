from pathlib import Path
from unittest import TestCase
from form_checker.utils.filename import (
    is_url,
    get_basename_with_suffix,
    strip_querystring,
)


class GetBasenameTests(TestCase):
    # def get_basename_with_suffix(path, suffix):
    base = str(Path.home())
    cwd = str(Path.cwd())
    file = str(Path.home() / "test.mp4")
    cwd_file = str(Path.cwd() / "test.mp4")

    def test_normal_path(self):
        assert (
            get_basename_with_suffix(self.file, "suffix") == "test_suffix.mp4"
        )

    def test_base_path(self):
        with self.assertRaises(IOError):
            get_basename_with_suffix(self.base, "suffix")

    def test_cwd_path(self):
        with self.assertRaises(IOError):
            get_basename_with_suffix(self.cwd, "suffix")

    def test_cwd_file(self):
        assert (
            get_basename_with_suffix(self.cwd_file, "suffix")
            == "test_suffix.mp4"
        )

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            get_basename_with_suffix(1, "suffix")


class IsURLTests(TestCase):
    # is_url(candidate: str) -> bool:
    def test_file_path(self):
        assert not is_url(str(Path.home() / "test.mp4"))

    def test_http(self):
        assert is_url("http://websitesname.com")

    def test_https(self):
        assert is_url("https://www.facebook.com/some-details-330002341216/")

    def test_ftp(self):
        assert not is_url("ftp://random.vib.slx/")

    def test_anchor(self):
        assert is_url("https://en.wikipedia.org/wiki/Internet#Terminology")

    def test_query_string(self):
        assert is_url(
            "http://host.company.com/showCompanyInfo?name=C%26H%20Sugar"
        )


class StripQStringTests(TestCase):
    # strip_querystring(url: str) -> str:
    def test_normal(self):
        assert (
            strip_querystring(
                "http://host.company.com/showCompanyInfo?name=C%26H%20Sugar"
            )
            == "http://host.company.com/showCompanyInfo"
        )

    def test_url(self):
        assert (
            strip_querystring(
                "https://en.wikipedia.org/wiki/Internet#Terminology"
            )
            == "https://en.wikipedia.org/wiki/Internet"
        )

    def test_file_path(self):
        path = str(Path.cwd() / "test.mp4")
        assert strip_querystring(path) == path or path.startswith(strip_querystring(path))
