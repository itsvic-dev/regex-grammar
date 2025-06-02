import re
from regex_grammar import parse_str

LANG_GRAMMAR = """
group langtag = language ["-" script] ["-" region]
group language = alpha{2,3}
group script = alpha{4}
group region = alpha{2} | digit{3}

def alpha = "[a-zA-Z]"
def digit = "[0-9]"
"""

tree = parse_str(LANG_GRAMMAR)
assert tree is not None
pattern = tree[0].to_regex("python")


def test_matches_en():
    match = re.fullmatch(pattern, "en")
    assert match is not None
    assert match.groups() == ("en", "en", None, None)


def test_matches_zh_CN():
    match = re.fullmatch(pattern, "zh-CN")
    assert match is not None
    assert match.groups() == ("zh-CN", "zh", None, "CN")


def test_matches_zh_Hans_CN():
    match = re.fullmatch(pattern, "zh-Hans-CN")
    assert match is not None
    assert match.groups() == ("zh-Hans-CN", "zh", "Hans", "CN")


def test_doesnt_match_invalid_lang():
    assert re.fullmatch(pattern, "en=US") is None
