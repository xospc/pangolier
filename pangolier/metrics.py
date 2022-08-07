from .common import indent_body
from .filters import _make_filter


class MetricBase:
    def to_str(self, pretty=False):
        raise NotImplementedError

    def __truediv__(self, other):
        return BinOp('/', self, other)


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


class BinOp(MetricBase):
    def __init__(self, op, first, second):
        self.op = op
        self.first = first
        self.second = second

    def to_str(self, pretty=False):
        return '%s %s %s' % (
            self.first.to_str(pretty=pretty),
            self.op,
            self.second.to_str(pretty=pretty),
        )
