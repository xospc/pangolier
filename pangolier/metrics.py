from .common import indent_body, format_modifier
from .filters import _make_filter


class MetricBase:
    def to_str(self, pretty=False):
        raise NotImplementedError

    def __add__(self, other):
        return BinOp('+', self, other)

    def __sub__(self, other):
        return BinOp('-', self, other)

    def __mul__(self, other):
        return BinOp('*', self, other)

    def __truediv__(self, other):
        return BinOp('/', self, other)

    def __mod__(self, other):
        return BinOp('%', self, other)

    def __xor__(self, other):
        return BinOp('^', self, other)


class Metric(MetricBase):
    def __init__(self, name):
        self.name = name

    def to_str(self, pretty=False):
        return self.name

    def filter(self, **kwargs):
        return FilteredMetric(self, [
            (k, _make_filter(v))
            for k, v in kwargs.items()
        ])


class FilteredMetric(MetricBase):
    def __init__(self, origin_metric, filters):
        self.origin_metric = origin_metric
        self.filters = filters

    def to_str(self, pretty=False):
        if not self.filters:
            return self.origin_metric.to_str(pretty=pretty)

        body_parts = [
            '%s%s' % (k, f.to_str(pretty=pretty))
            for k, f in self.filters
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

    def filter(self, **kwargs):
        append_filters = [
            (k, _make_filter(v))
            for k, v in kwargs.items()
        ]

        return FilteredMetric(
            self.origin_metric,
            self.filters + append_filters
        )


class GroupBase(MetricBase):
    modifier = ''

    def __init__(self, *labels):
        self.labels = labels

    def to_str(self, pretty=False):
        return format_modifier(self.modifier, self.labels, pretty=pretty)


class GroupLeft(GroupBase):
    modifier = 'group_left'


class GroupRight(GroupBase):
    modifier = 'group_right'


class BinOp(MetricBase):
    def __init__(
        self, op, first, second,
        *, on=None, ignoring=None, group=None,
    ):
        if on and ignoring:
            raise ValueError('can not specific both `on` and `ignoring`')

        self.op = op
        self.first = first
        self.second = second

        self.on = on
        self.ignoring = ignoring
        self.group = group

    def to_str(self, pretty=False):
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
