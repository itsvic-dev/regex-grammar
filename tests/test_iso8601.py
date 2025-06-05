import re
from .lib import load_from_examples

pattern = load_from_examples("iso8601.rg")


def test_matches_date():
    match = re.fullmatch(pattern, "2025-05-23")
    assert match is not None
