class Regexable:
    def to_regex(self, _format):
        raise NotImplementedError(f"{self.__class__.__name__}.to_regex()")


class Expr(Regexable):
    pass


class Def(Regexable):
    def __init__(self, name: str, children: list[Expr]):
        self.name = name
        self.children = children

    def __repr__(self):
        children_repr = " ".join(repr(child) for child in self.children)
        return f"{self.__class__.__name__.lower()[:-3]} {self.name} = {children_repr}"

    def to_regex(self, format):
        # to turn this into a regex, just concat the regexes of the children
        return "".join(expr.to_regex(format) for expr in self.children)


class GroupDef(Def):
    def to_regex(self, format):
        prefix = "P" if format == "python" else ""
        return f"(?{prefix}<{self.name}>{super().to_regex(format)})"


class NameDef(Def):
    # name defs, aka plain defs, should be non-capturing groups
    def to_regex(self, format):
        return f"(?:{super().to_regex(format)})"


class OrExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{repr(self.left)} | {repr(self.right)}"

    def to_regex(self, format):
        return f"(?:{self.left.to_regex(format)}|{self.right.to_regex(format)})"


class OptionalGroupExpr(Expr):
    def __init__(self, children: list[Expr]):
        self.children = children

    def __repr__(self):
        children_repr = " ".join(repr(child) for child in self.children)
        return f"[{children_repr}]"

    def to_regex(self, format):
        inner_regex = "".join(expr.to_regex(format) for expr in self.children)
        return f"(?:{inner_regex})?"


class RuleExpr(Expr):
    def __init__(self, rule: str | Def):
        self.rule = rule

    def __repr__(self):
        if isinstance(self.rule, Def):
            return self.rule.name
        return self.rule

    def to_regex(self, format):
        if isinstance(self.rule, Def):
            return self.rule.to_regex(format)
        else:
            raise Exception("rule should be resolved to a def")


class RuleRangeExpr(RuleExpr):
    def __init__(self, rule: str, min: str, max: str):
        super().__init__(rule)
        self.min = int(min)
        self.max = int(max)

    def __repr__(self):
        return f"{self.rule}{{{self.min},{self.max}}}"

    def to_regex(self, format):
        return super().to_regex(format) + f"{{{self.min},{self.max}}}"


class RuleCountExpr(RuleExpr):
    def __init__(self, rule: str, count: str):
        super().__init__(rule)
        self.count = int(count)

    def __repr__(self):
        return f"{self.rule}{{{self.count}}}"

    def to_regex(self, format):
        return super().to_regex(format) + f"{{{self.count}}}"


class LiteralExpr(Expr):
    def __init__(self, literal: str):
        self.literal = literal.strip('"')

    def __repr__(self):
        return f'"{self.literal}"'

    def to_regex(self, _format):
        return self.literal
