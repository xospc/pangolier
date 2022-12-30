from .common import indent_body
from .metrics import MetricBase


class FunctionBase(MetricBase):
    pass


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


def _format_arg(arg, pretty=False):
    if isinstance(arg, MetricBase):
        return arg.to_str(pretty=pretty)

    return str(arg)


class SimpleFunction(FunctionBase):
    name = 'unknown'

    def __init__(self, *argv):
        self.argv = argv

    def to_str(self, pretty=False):
        formatted_argv = [
            _format_arg(arg, pretty=pretty)
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


class HistogramQuantile(SimpleFunction):
    # deprecated, will be removed soon.
    # use `function` instead.
    name = 'histogram_quantile'


def function(name):
    return type(
        'simple_function_%s' % name,
        (SimpleFunction,),
        {'name': name}
    )


class RangeFunction(FunctionBase):
    name = 'unknown'

    def __init__(self, origin_metric, timespan):
        self.origin_metric = origin_metric
        self.timespan = timespan

    def to_str(self, pretty=False):
        body = self.origin_metric.to_str(pretty=pretty)

        if pretty:
            return '%s(\n%s[%s]\n)' % (
                self.name,
                indent_body(body),
                self.timespan
            )

        return '%s(%s[%s])' % (self.name, body, self.timespan)


class Rate(RangeFunction):
    # deprecated, will be removed soon.
    # use `range_function` instead.
    name = 'rate'


def range_function(name):
    return type(
        'range_function_%s' % name,
        (RangeFunction,),
        {'name': name}
    )
