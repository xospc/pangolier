from typing import Union


class FilterBase:
    expression: str

    def __init__(self, expression: str):
        self.expression = expression

    def to_str(self, pretty: bool = False) -> str:
        raise NotImplementedError


class EqualFilter(FilterBase):
    def to_str(self, pretty: bool = False) -> str:
        return '="%s"' % self.expression


class NotEqualFilter(FilterBase):
    def to_str(self, pretty: bool = False) -> str:
        return '!="%s"' % self.expression


class RegexpFilter(FilterBase):
    def to_str(self, pretty: bool = False) -> str:
        return '=~"%s"' % self.expression


FilterValueType = Union[str, FilterBase]
FilterTuple = tuple[str, FilterBase]


def _make_filter(value: FilterValueType) -> FilterBase:
    if isinstance(value, str):
        return EqualFilter(value)

    if isinstance(value, FilterBase):
        return value

    raise ValueError('cannot parse filter: %r' % value)
