from textwrap import dedent
from unittest import TestCase

from pangolier.metrics import Metric
from pangolier.functions import Rate, Sum, function


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

    def test_histogram_quantile_deprecated(self):
        from pangolier.functions import HistogramQuantile

        self._assert_pretty_equal(
            HistogramQuantile(
                0.9,
                Sum(
                    Rate(
                        Metric('http_request_duration_seconds_bucket'),
                        timespan='5m',
                    ),
                    by=('le',)
                )
            ),
            '''
                histogram_quantile(
                    0.9,
                    sum by(
                        le
                    )(
                        rate(
                            http_request_duration_seconds_bucket[5m]
                        )
                    )
                )
            '''
        )

    def test_histogram_quantile(self):
        histogram_quantile = function('histogram_quantile')

        self._assert_pretty_equal(
            histogram_quantile(
                0.9,
                Sum(
                    Rate(
                        Metric('http_request_duration_seconds_bucket'),
                        timespan='5m',
                    ),
                    by=('le',)
                )
            ),
            '''
                histogram_quantile(
                    0.9,
                    sum by(
                        le
                    )(
                        rate(
                            http_request_duration_seconds_bucket[5m]
                        )
                    )
                )
            '''
        )

    def test_bin_op(self):
        self._assert_pretty_equal(
            Rate(
                Metric('foo').filter(
                    group='canary'
                ),
                timespan='5m'
            ) / Rate(
                Metric('bar').filter(
                    group='canary'
                ),
                timespan='5m'
            ),
            '''
                rate(
                    foo{
                        group="canary"
                    }[5m]
                ) / rate(
                    bar{
                        group="canary"
                    }[5m]
                )
            '''
        )
