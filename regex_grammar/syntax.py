class Regexable:
    def to_regex(self, _format, _prefix):
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

    def to_regex(self, format, prefix=""):
        # to turn this into a regex, just concat the regexes of the children
        return "".join(expr.to_regex(format, prefix) for expr in self.children)


class GroupDef(Def):
    def to_regex(self, format, prefix=""):
        format_prefix = "P" if format == "python" else ""
        # append our name + the old prefix to future groups
        new_prefix = prefix + self.name + "_"
        if len(prefix + self.name) > 32:
            raise Exception(
                f"name of prefixed group {prefix + self.name} is too long (>32)"
            )
        return f"(?{format_prefix}<{prefix + self.name}>{super().to_regex(format, new_prefix)})"


class NameDef(Def):
    # name defs, aka plain defs, should be non-capturing groups
    def to_regex(self, format, prefix):
        # append our name + the old prefix to future groups
        new_prefix = prefix + self.name + "_"
        inner_regex = super().to_regex(format, new_prefix)
        # if we have only one child, we can skip the group
        if len(self.children) == 1:
            return inner_regex
        return f"(?:{inner_regex})"


class OrExpr(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{repr(self.left)} | {repr(self.right)}"

    def to_regex(self, format, prefix):
        return f"(?:{self.left.to_regex(format, prefix)}|{self.right.to_regex(format, prefix)})"


_GroupExpr__GROUP_COUNTER = 0


class GroupExpr(Expr):
    def __init__(self, children: list[Expr]):
        self.children = children

    def __repr__(self):
        children_repr = " ".join(repr(child) for child in self.children)
        return f"({children_repr})"

    def to_regex(self, format, prefix):
        global __GROUP_COUNTER
        # append our name + the old prefix to future groups
        new_prefix = prefix + str(__GROUP_COUNTER) + "_"
        __GROUP_COUNTER += 1
        inner_regex = "".join(
            expr.to_regex(format, new_prefix) for expr in self.children
        )
        # if we have only one child, we can skip the group
        if len(self.children) == 1:
            return inner_regex
        return f"(?:{inner_regex})"


class OptionalGroupExpr(Expr):
    def __init__(self, children: list[Expr]):
        self.children = children

    def __repr__(self):
        children_repr = " ".join(repr(child) for child in self.children)
        return f"[{children_repr}]"

    def to_regex(self, format, prefix):
        inner_regex = "".join(expr.to_regex(format, prefix) for expr in self.children)
        # if we have only one child, we can skip the group
        if len(self.children) == 1:
            return inner_regex + "?"
        return f"(?:{inner_regex})?"


class RuleExpr(Expr):
    def __init__(self, rule: str | Def):
        self.rule = rule

    def __repr__(self):
        if isinstance(self.rule, Def):
            return self.rule.name
        return self.rule

    def to_regex(self, format, prefix):
        if isinstance(self.rule, Def):
            return self.rule.to_regex(format, prefix)
        else:
            raise Exception(f"rule {self.rule} should be resolved to a def")


class RuleRangeExpr(RuleExpr):
    def __init__(self, rule: str, min: str, max: str):
        super().__init__(rule)
        self.min = int(min)
        self.max = int(max)

    def __repr__(self):
        return f"{self.rule}{{{self.min},{self.max}}}"

    def to_regex(self, format, prefix):
        return super().to_regex(format, prefix) + f"{{{self.min},{self.max}}}"


class RuleCountExpr(RuleExpr):
    def __init__(self, rule: str, count: str):
        super().__init__(rule)
        self.count = int(count)

    def __repr__(self):
        return f"{self.rule}{{{self.count}}}"

    def to_regex(self, format, prefix):
        return super().to_regex(format, prefix) + f"{{{self.count}}}"


class LiteralExpr(Expr):
    def __init__(self, literal: str):
        self.literal = literal.strip('"')

    def __repr__(self):
        return f'"{self.literal}"'

    def to_regex(self, _format, _prefix):
        return self.literal
