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
    # deprecated, will be removed soon.
    # use `function` instead.
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


class SimpleFunction(FunctionBase):
    name = 'unknown'

    def __init__(self, *argv):
        self.argv = argv

    def _format_arg(self, arg, pretty=False):
        if isinstance(arg, MetricBase):
            return arg.to_str(pretty=pretty)

        return str(arg)

    def to_str(self, pretty=False):
        formatted_argv = [
            self._format_arg(arg, pretty=pretty)
            for arg in self.argv
        ]

        if pretty:
            return '%s(\n%s\n)' % (
                self.name,
                ',\n'.join([
                    indent_body(arg)
                    for arg in formatted_argv
                ])
            )

        return '%s(%s)' % (
            self.name, ', '.join(formatted_argv)
        )


def function(name):
    return type(
        'simple_function_%s' % name,
        (SimpleFunction,),
        {'name': name}
    )
