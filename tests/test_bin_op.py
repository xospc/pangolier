from unittest import TestCase

from pangolier.metrics import Metric
from pangolier.functions import range_function


class TestBinOp(TestCase):
    def test_metrics(self):
        self.assertEqual(
            (Metric('foo') / Metric('bar')).to_str(),
            'foo / bar'
        )

        self.assertEqual(
            (Metric('foo') - Metric('bar') / Metric('biz')).to_str(),
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
