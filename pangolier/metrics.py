from abc import abstractmethod
from collections.abc import Callable

from .common import indent_body
from .filters import (
    make_filter_clause,
    FilterValueType, FilterClause,
)


def _make_bin_op_method(operator: str) -> Callable[
    ['MetricBase', 'MetricBase'], 'MetricBase'
]:
    def bin_op_method(self: 'MetricBase', other: 'MetricBase') -> 'MetricBase':
        from .bin_op import BinOp

        return BinOp(operator, self, other)

    return bin_op_method


class MetricBase:
    @abstractmethod
    def to_str(self, pretty: bool = False) -> str:
        raise NotImplementedError

    __add__ = _make_bin_op_method('+')
    __sub__ = _make_bin_op_method('-')
    __mul__ = _make_bin_op_method('*')
    __truediv__ = _make_bin_op_method('/')
    __mod__ = _make_bin_op_method('%')
    __xor__ = _make_bin_op_method('^')
    __lt__ = _make_bin_op_method('<')
    __le__ = _make_bin_op_method('<=')
    __gt__ = _make_bin_op_method('>')
    __ge__ = _make_bin_op_method('>=')
    __eq__ = _make_bin_op_method('=')  # type: ignore[assignment]
    __ne__ = _make_bin_op_method('!=')  # type: ignore[assignment]


class FilterableMetricBase(MetricBase):
    @abstractmethod
    def filter(self, **kwargs: FilterValueType) -> 'FilteredMetric':
        raise NotImplementedError


class Metric(FilterableMetricBase):
    name: str

    def __init__(self, name: str):
        self.name = name

    def to_str(self, pretty: bool = False) -> str:
        return self.name

    def filter(self, **kwargs: FilterValueType) -> 'FilteredMetric':
        return FilteredMetric(self, [
            make_filter_clause(k, v)
            for k, v in kwargs.items()
        ])

    def where(self, *argv: FilterClause) -> 'FilteredMetric':
        return FilteredMetric(self, list(argv))


class FilteredMetric(FilterableMetricBase):
    origin_metric: MetricBase
    filters: list[FilterClause]

    def __init__(self, origin_metric: MetricBase, filters: list[FilterClause]):
        self.origin_metric = origin_metric
        self.filters = filters

    def to_str(self, pretty: bool = False) -> str:
        if not self.filters:
            return self.origin_metric.to_str(pretty=pretty)

        body_parts = [
            f.to_str(pretty=pretty)
            for f in self.filters
        ]

        if pretty:
            return '%s{\n%s\n}' % (
                self.origin_metric.to_str(),
                indent_body(',\n'.join(body_parts))
            )

        return '%s{%s}' % (
            self.origin_metric.to_str(),
            ', '.join(body_parts)
        )

    def filter(self, **kwargs: FilterValueType) -> 'FilteredMetric':
        append_filters = [
            make_filter_clause(k, v)
            for k, v in kwargs.items()
        ]

        return FilteredMetric(
            self.origin_metric,
            self.filters + append_filters
        )

    def where(self, *argv: FilterClause) -> 'FilteredMetric':
        return FilteredMetric(self, self.filters + list(argv))
