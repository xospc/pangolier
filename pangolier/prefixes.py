from .filters import _make_filter
from .metrics import Metric, FilteredMetric


class PrefixBase:
    def add_suffix(self, suffix):
        raise NotImplementedError


class MetricPrefix(PrefixBase):
    def __init__(self, name):
        self.name = name

    def filter(self, **kwargs):
        return FilteredMetricPrefix(self, [
            (k, _make_filter(v))
            for k, v in kwargs.items()
        ])

    def add_suffix(self, suffix):
        return Metric(
            name=self.name + suffix
        )


class FilteredMetricPrefix(PrefixBase):
    def __init__(self, origin_metric, filters):
        self.origin_metric = origin_metric
        self.filters = filters

    def filter(self, **kwargs):
        append_filters = [
            (k, _make_filter(v))
            for k, v in kwargs.items()
        ]

        return FilteredMetricPrefix(
            self.origin_metric,
            self.filters + append_filters
        )

    def add_suffix(self, suffix):
        return FilteredMetric(
            origin_metric=self.origin_metric.add_suffix(suffix),
            filters=self.filters
        )
