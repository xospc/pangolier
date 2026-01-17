from typing import Union

from .common import indent_body
from .metrics import MetricBase

ArgType = Union[int, float, str, MetricBase]


class FunctionBase(MetricBase):
    pass


def _format_arg(arg: ArgType, pretty: bool = False) -> str:
    if isinstance(arg, MetricBase):
        return arg.to_str(pretty=pretty)

    if isinstance(arg, str):
        return '"%s"' % arg

    return str(arg)


class SimpleFunction(FunctionBase):
    argv: list[ArgType]

    name = 'unknown'

    def __init__(self, *argv: ArgType):
        self.argv = list(argv)

    def to_str(self, pretty: bool = False) -> str:
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


def function(name: str) -> type[SimpleFunction]:
    return type(
        'simple_function_%s' % name,
        (SimpleFunction,),
        {'name': name}
    )


class RangeFunction(FunctionBase):
    origin_metric: MetricBase
    timespan: str

    name = 'unknown'

    def __init__(self, origin_metric: MetricBase, timespan: str):
        self.origin_metric = origin_metric
        self.timespan = timespan

    def to_str(self, pretty: bool = False) -> str:
        body = self.origin_metric.to_str(pretty=pretty)

        if pretty:
            return '%s(\n%s[%s]\n)' % (
                self.name,
                indent_body(body),
                self.timespan
            )

        return '%s(%s[%s])' % (self.name, body, self.timespan)


def range_function(name: str) -> type[RangeFunction]:
    return type(
        'range_function_%s' % name,
        (RangeFunction,),
        {'name': name}
    )


class AggregationOperator(FunctionBase):
    argv: list[ArgType]
    kwargs: dict[str, list[str]]

    name = 'unknown'

    def __init__(self, *argv: ArgType, **kwargs: list[str]):
        self.argv = list(argv)

        if len(kwargs) > 1:
            raise ValueError('too many kwargs: %s' % kwargs)

        self.kwargs = kwargs

    def _make_clause(self, pretty: bool = False) -> str:
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

    def to_str(self, pretty: bool = False) -> str:
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


def aggregation_operator(name: str) -> type[AggregationOperator]:
    return type(
        'aggregation_operator_%s' % name,
        (AggregationOperator,),
        {'name': name}
    )
