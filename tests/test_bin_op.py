from functools import reduce

from unittest import TestCase

from pangolier.metrics import MetricBase, Metric
from pangolier.bin_op import BinOp, GroupLeft, GroupRight
from pangolier.functions import range_function

from .utils import make_multiply_func


class TestBinOp(TestCase):
    def _assert_metric_str(self, metric: MetricBase, query: str) -> None:
        self.assertEqual(
            metric.to_str(),
            query
        )

    def test_addition(self) -> None:
        self._assert_metric_str(
            Metric('foo') + Metric('bar'),
            'foo + bar'
        )

    def test_subtraction(self) -> None:
        self._assert_metric_str(
            Metric('foo') - Metric('bar'),
            'foo - bar'
        )

    def test_multiplication(self) -> None:
        self._assert_metric_str(
            Metric('foo') * Metric('bar'),
            'foo * bar'
        )

    def test_division(self) -> None:
        self._assert_metric_str(
            Metric('foo') / Metric('bar'),
            'foo / bar'
        )

    def test_modulo(self) -> None:
        self._assert_metric_str(
            Metric('foo') % Metric('bar'),
            'foo % bar'
        )

    def test_exponentiation(self) -> None:
        self._assert_metric_str(
            Metric('foo') ^ Metric('bar'),
            'foo ^ bar'
        )

    def test_metrics(self) -> None:
        self._assert_metric_str(
            Metric('foo') - Metric('bar') / Metric('biz'),
            'foo - bar / biz'
        )

    def test_precedence(self) -> None:
        self._assert_metric_str(
            Metric('foo') * (Metric('bar') > Metric('0')) * Metric('qux'),
            'foo * (bar > 0) * qux',
        )

    def test_filters(self) -> None:
        self.assertEqual(
            (
                Metric('foo').filter(
                    group='canary'
                ) / Metric('bar').filter(
                    group='canary'
                )
            ).to_str(),
            'foo{group="canary"} / bar{group="canary"}'
        )

    def test_functions(self) -> None:
        rate = range_function('rate')

        self.assertEqual(
            (
                rate(
                    Metric('foo').filter(
                        group='canary'
                    ),
                    timespan='5m'
                ) / rate(
                    Metric('bar').filter(
                        group='canary'
                    ),
                    timespan='5m'
                )
            ).to_str(),
            'rate(foo{group="canary"}[5m]) / rate(bar{group="canary"}[5m])'
        )

    def test_on(self) -> None:
        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=['interface']
            ),
            'foo * on(interface) bar',
        )

        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=['interface', 'job']
            ),
            'foo * on(interface, job) bar',
        )

    def test_ignoring(self) -> None:
        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                ignoring=['interface', 'job']
            ),
            'foo * ignoring(interface, job) bar',
        )

        with self.assertRaises(ValueError):
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=['interface'],
                ignoring=['job']
            )

    def test_group(self) -> None:
        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                group=GroupLeft(),
            ),
            'foo * group_left bar',
        )

        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=['interface', 'job'],
                group=GroupRight(),
            ),
            'foo * on(interface, job) group_right bar',
        )

        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=['interface', 'job'],
                group=GroupLeft('node', 'resource'),
            ),
            'foo * on(interface, job) group_left(node, resource) bar',
        )

    def test_group_with_precedence(self) -> None:
        self._assert_metric_str(
            reduce(
                make_multiply_func(on=['name'], group=GroupLeft()),
                [
                    Metric('foo'),
                    Metric('bar') > Metric('0'),
                    Metric('qux'),
                ]
            ),
            'foo * on(name) group_left() (bar > 0) * on(name) group_left qux',
        )

    def test_group_with_precedence_another(self) -> None:
        self._assert_metric_str(
            reduce(
                make_multiply_func(on=['name'], group=GroupLeft()),
                [
                    Metric('bar') > Metric('0'),
                    Metric('foo'),
                    Metric('qux'),
                ]
            ),
            '(bar > 0) * on(name) group_left foo * on(name) group_left qux',
        )

    def test_group_with_precedence_reverse(self) -> None:
        self._assert_metric_str(
            reduce(
                make_multiply_func(
                    on=['name'], group=GroupLeft(), reverse=True,
                ),
                [
                    Metric('qux'),
                    Metric('bar') > Metric('0'),
                    Metric('foo'),
                ]
            ),
            'foo * on(name) group_left() (bar > 0) * on(name) group_left qux',
        )
