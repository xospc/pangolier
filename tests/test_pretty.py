from textwrap import dedent
from unittest import TestCase

from pangolier.metrics import Metric
from pangolier.functions import Rate, Sum


class TestPretty(TestCase):
    def _assert_pretty_equal(self, metric, query):
        self.assertEqual(
            metric.to_str(pretty=True),
            dedent(query).strip(),
        )

    def test_simple_metric(self):
        self._assert_pretty_equal(
            Metric('http_requests_total'),
            'http_requests_total',
        )

    def test_metric_with_filters(self):
        self._assert_pretty_equal(
            Metric('http_requests_total').filter(
                job='prometheus',
                group='canary'
            ),
            '''
                http_requests_total{
                    job="prometheus",
                    group="canary"
                }
            '''
        )

    def test_rate(self):
        self._assert_pretty_equal(
            Rate(Metric('http_requests_total'), timespan='5m'),
            '''
                rate(
                    http_requests_total[5m]
                )
            '''
        )

    def test_rate_with_filter(self):
        self._assert_pretty_equal(
            Rate(
                Metric('http_requests_total').filter(
                    job='prometheus',
                    group='canary'
                ),
                timespan='5m'
            ),
            '''
                rate(
                    http_requests_total{
                        job="prometheus",
                        group="canary"
                    }[5m]
                )
            '''
        )

    def test_sum(self):
        self._assert_pretty_equal(
            Sum(Metric('http_requests_total')),
            '''
                sum(
                    http_requests_total
                )
            '''
        )

    def test_sum_by(self):
        self._assert_pretty_equal(
            Sum(
                Metric('http_requests_total'),
                by=('job', 'group'),
            ),
            '''
                sum by(
                    job, group
                )(
                    http_requests_total
                )
            '''
        )

    def test_sum_by_rate(self):
        self._assert_pretty_equal(
            Sum(
                Rate(
                    Metric('http_requests_total'),
                    timespan='5m'
                ),
                by=('job', 'group'),
            ),
            '''
                sum by(
                    job, group
                )(
                    rate(
                        http_requests_total[5m]
                    )
                )
            '''
        )

    def test_sum_by_rate_with_filter(self):
        self._assert_pretty_equal(
            Sum(
                Rate(
                    Metric('http_requests_total').filter(
                        job='prometheus',
                    ),
                    timespan='5m'
                ),
                by=('group',)
            ),
            '''
                sum by(
                    group
                )(
                    rate(
                        http_requests_total{
                            job="prometheus"
                        }[5m]
                    )
                )
            '''
        )
