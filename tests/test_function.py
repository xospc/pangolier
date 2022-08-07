from unittest import TestCase

from pangolier.metrics import Metric
from pangolier.functions import Rate, Sum, HistogramQuantile


class TestFunction(TestCase):
    def test_rate(self):
        self.assertEqual(
            Rate(Metric('http_requests_total'), timespan='5m').to_str(),
            'rate(http_requests_total[5m])'
        )

    def test_rate_with_filter(self):
        self.assertEqual(
            Rate(
                Metric('http_requests_total').filter(
                    job='prometheus',
                    group='canary'
                ),
                timespan='5m'
            ).to_str(),
            'rate(http_requests_total{job="prometheus", group="canary"}[5m])'
        )

    def test_sum(self):
        self.assertEqual(
            Sum(Metric('http_requests_total')).to_str(),
            'sum(http_requests_total)'
        )

    def test_sum_by(self):
        self.assertEqual(
            Sum(
                Metric('http_requests_total'),
                by=('job', 'group'),
            ).to_str(),
            'sum by(job, group)(http_requests_total)'
        )

    def test_sum_by_rate(self):
        self.assertEqual(
            Sum(
                Rate(
                    Metric('http_requests_total'),
                    timespan='5m'
                ),
                by=('job', 'group'),
            ).to_str(),
            'sum by(job, group)(rate(http_requests_total[5m]))'
        )

    def test_sum_by_rate_with_filter(self):
        self.assertEqual(
            Sum(
                Rate(
                    Metric('http_requests_total').filter(
                        job='prometheus',
                    ),
                    timespan='5m'
                ),
                by=('group',)
            ).to_str(),
            'sum by(group)(rate(http_requests_total{job="prometheus"}[5m]))'  # noqa
        )

    def test_histogram_quantile(self):
        self.assertEqual(
            HistogramQuantile(
                0.9,
                Sum(
                    Rate(
                        Metric('http_request_duration_seconds_bucket'),
                        timespan='5m',
                    ),
                    by=('le',)
                )
            ).to_str(),
            'histogram_quantile(0.9, sum by(le)(rate(http_request_duration_seconds_bucket[5m])))'  # noqa
        )
