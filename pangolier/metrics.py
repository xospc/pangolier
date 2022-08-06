from .filters import _make_filter


class MetricBase:
    def to_str(self):
        raise NotImplementedError


class Metric(MetricBase):
    def __init__(self, name):
        self.name = name

    def to_str(self):
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

    def to_str(self):
        return '%s{%s}' % (
            self.origin_metric.to_str(),
            ', '.join([
                '%s%s' % (k, f.to_str())
                for k, f in self.filters
            ])
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
