from .common import indent_body
from .metrics import MetricBase


class FunctionBase(MetricBase):
    pass


class Rate(FunctionBase):
    # Should I give timespan a default value.
    # Maybe 5m?
    def __init__(self, origin_metric, timespan):
        self.origin_metric = origin_metric
        self.timespan = timespan

    def to_str(self, pretty=False):
        body = self.origin_metric.to_str(pretty=pretty)

        if pretty:
            return 'rate(\n%s[%s]\n)' % (
                indent_body(body),
                self.timespan
            )

        return 'rate(%s[%s])' % (body, self.timespan)


class Sum(FunctionBase):
    def __init__(self, origin_metric, by=None):
        self.origin_metric = origin_metric
        self.by = by

    def to_str(self, pretty=False):
        body = self.origin_metric.to_str(pretty=pretty)

        if self.by:
            by_str = ', '.join(self.by)

            if pretty:
                return 'sum by(\n%s\n)(\n%s\n)' % (
                    indent_body(by_str),
                    indent_body(body)
                )
            return 'sum by(%s)(%s)' % (
                by_str,
                body
            )

        if pretty:
            return 'sum(\n%s\n)' % (
                indent_body(body),
            )

        return 'sum(%s)' % body


class HistogramQuantile(FunctionBase):
    def __init__(self, quantile, origin_metric):
        self.quantile = quantile
        self.origin_metric = origin_metric

    def to_str(self, pretty=False):
        body = self.origin_metric.to_str(pretty=pretty)

        if pretty:
            return 'histogram_quantile(\n%s,\n%s\n)' % (
                indent_body(str(self.quantile)),
                indent_body(body),
            )

        return 'histogram_quantile(%s, %s)' % (
            self.quantile, body
        )
