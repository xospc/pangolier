from abc import abstractmethod
from typing import Optional

from .common import indent_body, format_modifier
from .filters import (
    make_filter_clause,
    FilterValueType, FilterClause,
)


class MetricBase:
    @abstractmethod
    def to_str(self, pretty: bool = False) -> str:
        raise NotImplementedError

    def __add__(self, other: 'MetricBase') -> 'MetricBase':
        return BinOp('+', self, other)

    def __sub__(self, other: 'MetricBase') -> 'MetricBase':
        return BinOp('-', self, other)

    def __mul__(self, other: 'MetricBase') -> 'MetricBase':
        return BinOp('*', self, other)

    def __truediv__(self, other: 'MetricBase') -> 'MetricBase':
        return BinOp('/', self, other)

    def __mod__(self, other: 'MetricBase') -> 'MetricBase':
        return BinOp('%', self, other)

    def __xor__(self, other: 'MetricBase') -> 'MetricBase':
        return BinOp('^', self, other)


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


class GroupBase(MetricBase):
    modifier = ''
    labels: list[str]

    def __init__(self, *labels: str):
        self.labels = list(labels)

    def to_str(self, pretty: bool = False) -> str:
        return format_modifier(self.modifier, self.labels, pretty=pretty)


class GroupLeft(GroupBase):
    modifier = 'group_left'


class GroupRight(GroupBase):
    modifier = 'group_right'


class BinOp(MetricBase):
    op: str
    first: MetricBase
    second: MetricBase

    on: Optional[list[str]]
    ignoring: Optional[list[str]]
    group: Optional[GroupBase]

    def __init__(
        self,
        op: str,
        first: MetricBase,
        second: MetricBase,
        *,
        on: Optional[list[str]] = None,
        ignoring: Optional[list[str]] = None,
        group: Optional[GroupBase] = None,
    ):
        if on and ignoring:
            raise ValueError('can not specific both `on` and `ignoring`')

        self.op = op
        self.first = first
        self.second = second

        self.on = on
        self.ignoring = ignoring
        self.group = group

    def to_str(self, pretty: bool = False) -> str:
        parts = []

        parts.append(self.first.to_str(pretty=pretty))
        parts.append(self.op)

        if self.on:
            parts.append(
                format_modifier('on', self.on, pretty=pretty)
            )

        if self.ignoring:
            parts.append(
                format_modifier('ignoring', self.ignoring, pretty=pretty)
            )

        if self.group:
            parts.append(self.group.to_str(pretty=pretty))

        parts.append(self.second.to_str(pretty=pretty))

        return ' '.join(parts)
