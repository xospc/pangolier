from .filters import make_filter_clause, FilterValueType, FilterClause
from .metrics import MetricBase, Metric, FilteredMetric


class PrefixBase:
    def add_suffix(self, suffix: str) -> MetricBase:
        raise NotImplementedError


class MetricPrefix(PrefixBase):
    name: str

    def __init__(self, name: str):
        self.name = name

    def filter(self, **kwargs: FilterValueType) -> 'FilteredMetricPrefix':
        return FilteredMetricPrefix(self, [
            make_filter_clause(k, v)
            for k, v in kwargs.items()
        ])

    def add_suffix(self, suffix: str) -> Metric:
        return Metric(
            name=self.name + suffix
        )


class FilteredMetricPrefix(PrefixBase):
    origin_metric: MetricPrefix
    filters: list[FilterClause]

    def __init__(
        self,
        origin_metric: MetricPrefix,
        filters: list[FilterClause]
    ):
        self.origin_metric = origin_metric
        self.filters = filters

    def filter(self, **kwargs: FilterValueType) -> 'FilteredMetricPrefix':
        append_filters = [
            make_filter_clause(k, v)
            for k, v in kwargs.items()
        ]

        return FilteredMetricPrefix(
            self.origin_metric,
            self.filters + append_filters
        )

    def add_suffix(self, suffix: str) -> FilteredMetric:
        return FilteredMetric(
            origin_metric=self.origin_metric.add_suffix(suffix),
            filters=self.filters
        )
