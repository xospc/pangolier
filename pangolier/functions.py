from .common import indent_body
from .metrics import MetricBase


class FunctionBase(MetricBase):
    pass


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


class AggregationOperator(FunctionBase):
    name = 'unknown'

    def __init__(self, *argv, **kwargs):
        self.argv = argv

        if len(kwargs) > 1:
            raise ValueError('too many kwargs: %s' % kwargs)

        self.kwargs = kwargs

    def _make_clause(self, pretty=False):
        if self.kwargs:
            key, value = next(iter(self.kwargs.items()))

            body = ', '.join(value)

            if pretty:
                return ' %s(\n%s\n)' % (
                    key,
                    indent_body(body)
                )

            return ' %s(%s)' % (key, body)

        return ''

    def to_str(self, pretty=False):
        clause = self._make_clause(pretty=pretty)

        formatted_argv = [
            _format_arg(arg, pretty=pretty)
            for arg in self.argv
        ]

        if pretty:
            return '%s%s(\n%s\n)' % (
                self.name,
                clause,
                ',\n'.join([
                    indent_body(arg)
                    for arg in formatted_argv
                ])
            )

        return '%s%s(%s)' % (
            self.name, clause, ', '.join(formatted_argv)
        )


class Sum(AggregationOperator):
    # deprecated, will be removed soon.
    # use `aggregation_operator` instead.
    name = 'sum'


def aggregation_operator(name):
    return type(
        'aggregation_operator_%s' % name,
        (AggregationOperator,),
        {'name': name}
    )
