import io
import logging
import tokenize
from pegen.tokenizer import Tokenizer

from . import syntax as s
from .parser import GeneratedParser

logger = logging.getLogger("regex_grammar.parser_wrapper")


def parse_file(file: io.TextIOBase) -> list[s.Def] | None:
    tokengen = tokenize.generate_tokens(file.readline)
    tokenizer = Tokenizer(tokengen)
    parser = GeneratedParser(tokenizer)
    tree = parser.start()

    if not tree:
        raise parser.make_syntax_error("invalid syntax")

    logger.debug(f"got tree {tree}")

    # go through the tree, find all RuleExprs and resolve the rule names to Defs
    defs = {d.name: d for d in tree}

    def resolve_rule_defs_in_expr(expr: s.Expr):
        if isinstance(expr, s.RuleExpr):
            d = defs[expr.rule]
            logger.debug(f"resolved rule def `{expr.rule}' to `{d}'")
            expr.rule = d
        elif isinstance(expr, s.OrExpr):
            resolve_rule_defs_in_expr(expr.left)
            resolve_rule_defs_in_expr(expr.right)

    def resolve_rule_defs_in_exprs(exprs: list[s.Expr]):
        for expr in exprs:
            # all exprs which have children
            if hasattr(expr, "children"):
                resolve_rule_defs_in_exprs(expr.children)
            else:
                resolve_rule_defs_in_expr(expr)

    for d in tree:
        resolve_rule_defs_in_exprs(d.children)

    return tree


def parse_str(content: str) -> list[s.Def] | None:
    return parse_file(io.StringIO(content))
