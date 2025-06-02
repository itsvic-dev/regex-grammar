import sys
import tokenize
import argparse
from pprint import pprint
from pegen.tokenizer import Tokenizer

from . import syntax as s
from .parser import GeneratedParser


# keeps the scope clean
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show detailed debug information"
    )
    return parser.parse_args()


def main_cli():
    args = get_args()

    def debug(msg: str, obj: object | None = None):
        if args.verbose:
            print("[DEBUG]", msg, end=" " if obj else None)
            if obj:
                pprint(obj)

    filename = args.filename
    if filename == "-":
        filename = "<stdin>"
        file = sys.stdin
    else:
        file = open(filename)
    tokengen = tokenize.generate_tokens(file.readline)
    tokenizer = Tokenizer(tokengen)
    parser = GeneratedParser(tokenizer)
    tree = parser.start()
    file.close()

    debug("got tree", tree)

    # go through the tree, find all RuleExprs and resolve the rule names to Defs
    defs = {d.name: d for d in tree}

    def resolve_rule_defs_in_expr(expr: s.Expr):
        if isinstance(expr, s.RuleExpr):
            d = defs[expr.rule]
            debug(f"resolved rule def `{expr.rule}' to `{d}'")
            expr.rule = d

    def resolve_rule_defs_in_exprs(exprs: list[s.Expr]):
        for expr in exprs:
            # all exprs which have children
            if hasattr(expr, "children"):
                resolve_rule_defs_in_exprs(expr.children)
            elif isinstance(expr, s.OrExpr):
                resolve_rule_defs_in_expr(expr.left)
                resolve_rule_defs_in_expr(expr.right)
            else:
                resolve_rule_defs_in_expr(expr)

    for d in tree:
        resolve_rule_defs_in_exprs(d.children)

    # grab the first def (the 'start') and to_regex() it
    # we get its superclass first so that we dont get the extra group around it
    start = tree[0]
    print(super(s.GroupDef, start).to_regex())
