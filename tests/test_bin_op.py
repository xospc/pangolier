from unittest import TestCase

from pangolier.metrics import Metric
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
