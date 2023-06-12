from unittest import TestCase

from pangolier.metrics import Metric, BinOp, GroupLeft, GroupRight
from pangolier.functions import range_function


class TestBinOp(TestCase):
    def _assert_metric_str(self, metric, query):
        self.assertEqual(
            metric.to_str(),
            query
        )

    def test_addition(self):
        self._assert_metric_str(
            Metric('foo') + Metric('bar'),
            'foo + bar'
        )

    def test_subtraction(self):
        self._assert_metric_str(
            Metric('foo') - Metric('bar'),
            'foo - bar'
        )

    def test_multiplication(self):
        self._assert_metric_str(
            Metric('foo') * Metric('bar'),
            'foo * bar'
        )

    def test_division(self):
        self._assert_metric_str(
            Metric('foo') / Metric('bar'),
            'foo / bar'
        )

    def test_modulo(self):
        self._assert_metric_str(
            Metric('foo') % Metric('bar'),
            'foo % bar'
        )

    def test_exponentiation(self):
        self._assert_metric_str(
            Metric('foo') ^ Metric('bar'),
            'foo ^ bar'
        )

    def test_metrics(self):
        self._assert_metric_str(
            Metric('foo') - Metric('bar') / Metric('biz'),
            'foo - bar / biz'
        )

    def test_filters(self):
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

    def test_functions(self):
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

    def test_on(self):
        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=('interface',)
            ),
            'foo * on(interface) bar',
        )

        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=('interface', 'job')
            ),
            'foo * on(interface, job) bar',
        )

    def test_ignoring(self):
        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                ignoring=('interface', 'job')
            ),
            'foo * ignoring(interface, job) bar',
        )

        with self.assertRaises(ValueError):
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=('interface',),
                ignoring=('job',)
            )

    def test_group(self):
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
                on=('interface', 'job'),
                group=GroupRight(),
            ),
            'foo * on(interface, job) group_right bar',
        )

        self._assert_metric_str(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=('interface', 'job'),
                group=GroupLeft('node', 'resource'),
            ),
            'foo * on(interface, job) group_left(node, resource) bar',
        )
