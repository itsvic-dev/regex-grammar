import os
from regex_grammar import parse_file


def load_from_examples(path: str):
    with open(os.path.join(os.path.dirname(__file__), "../examples", path)) as file:
        tree = parse_file(file)
    assert tree is not None
    return super(type(tree[0]), tree[0]).to_regex("python")
