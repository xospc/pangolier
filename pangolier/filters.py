from dataclasses import dataclass
from typing import Union, ClassVar


@dataclass(frozen=True)
class FilterClause:
    label: str
    op: str
    expression: str

    def to_str(self, pretty: bool = False) -> str:
        return '%s%s"%s"' % (self.label, self.op, self.expression)


class FilterBase:
    op: ClassVar[str]
    expression: str

    def __init__(self, expression: str):
        self.expression = expression


class EqualFilter(FilterBase):
    op = '='


class NotEqualFilter(FilterBase):
    op = '!='


class RegexpFilter(FilterBase):
    op = '=~'


class NotRegexpFilter(FilterBase):
    op = '!~'


FilterValueType = Union[str, FilterBase]
FilterTuple = tuple[str, FilterBase]


def _make_filter(value: FilterValueType) -> FilterBase:
    if isinstance(value, str):
        return EqualFilter(value)

    if isinstance(value, FilterBase):
        return value

    raise ValueError('cannot parse filter: %r' % value)


def make_filter_clause(label: str, value: FilterValueType) -> FilterClause:
    f = _make_filter(value)
    return FilterClause(label, f.op, f.expression)
