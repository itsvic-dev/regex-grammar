import re
from .lib import load_from_examples

pattern = load_from_examples("simple-bcp47.rg")


def test_matches_en():
    match = re.fullmatch(pattern, "en")
    assert match is not None
    assert match.groups() == ("en", None, None)


def test_matches_zh_CN():
    match = re.fullmatch(pattern, "zh-CN")
    assert match is not None
    assert match.groups() == ("zh", None, "CN")


def test_matches_zh_Hans_CN():
    match = re.fullmatch(pattern, "zh-Hans-CN")
    assert match is not None
    assert match.groups() == ("zh", "Hans", "CN")


def test_doesnt_match_invalid_lang():
    assert re.fullmatch(pattern, "en=US") is None
