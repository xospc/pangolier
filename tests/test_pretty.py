from textwrap import dedent
from unittest import TestCase

from pangolier.metrics import MetricBase, Metric, BinOp, GroupLeft
from pangolier.functions import (
    function, range_function, aggregation_operator as aggr,
)


class TestPretty(TestCase):
    def _assert_pretty_equal(self, metric: MetricBase, query: str) -> None:
        self.assertEqual(
            metric.to_str(pretty=True),
            dedent(query).strip(),
        )

    def test_simple_metric(self) -> None:
        self._assert_pretty_equal(
            Metric('http_requests_total'),
            'http_requests_total',
        )

    def test_metric_with_filters(self) -> None:
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

    def test_rate(self) -> None:
        rate = range_function('rate')

        self._assert_pretty_equal(
            rate(Metric('http_requests_total'), timespan='5m'),
            '''
                rate(
                    http_requests_total[5m]
                )
            '''
        )

    def test_increase(self) -> None:
        increase = range_function('increase')

        self._assert_pretty_equal(
            increase(Metric('http_requests_total'), timespan='5m'),
            '''
                increase(
                    http_requests_total[5m]
                )
            '''
        )

    def test_rate_with_filter(self) -> None:
        rate = range_function('rate')

        self._assert_pretty_equal(
            rate(
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

    def test_sum(self) -> None:
        sum_ = aggr('sum')

        self._assert_pretty_equal(
            sum_(Metric('http_requests_total')),
            '''
                sum(
                    http_requests_total
                )
            '''
        )

    def test_sum_by(self) -> None:
        sum_ = aggr('sum')

        self._assert_pretty_equal(
            sum_(
                Metric('http_requests_total'),
                by=['job', 'group'],
            ),
            '''
                sum by(
                    job, group
                )(
                    http_requests_total
                )
            '''
        )

    def test_avg_without(self) -> None:
        avg = aggr('avg')

        self._assert_pretty_equal(
            avg(
                Metric('http_requests_total'),
                without=['job', 'group'],
            ),
            '''
                avg without(
                    job, group
                )(
                    http_requests_total
                )
            '''
        )

    def test_sum_by_rate(self) -> None:
        rate = range_function('rate')
        sum_ = aggr('sum')

        self._assert_pretty_equal(
            sum_(
                rate(
                    Metric('http_requests_total'),
                    timespan='5m'
                ),
                by=['job', 'group'],
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

    def test_sum_by_rate_with_filter(self) -> None:
        rate = range_function('rate')
        sum_ = aggr('sum')

        self._assert_pretty_equal(
            sum_(
                rate(
                    Metric('http_requests_total').filter(
                        job='prometheus',
                    ),
                    timespan='5m'
                ),
                by=['group']
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

    def test_histogram_quantile(self) -> None:
        histogram_quantile = function('histogram_quantile')
        rate = range_function('rate')
        sum_ = aggr('sum')

        self._assert_pretty_equal(
            histogram_quantile(
                0.9,
                sum_(
                    rate(
                        Metric('http_request_duration_seconds_bucket'),
                        timespan='5m',
                    ),
                    by=['le']
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

    def test_bin_op(self) -> None:
        rate = range_function('rate')

        self._assert_pretty_equal(
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

    def test_bin_op_with_on_group(self) -> None:
        self._assert_pretty_equal(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=['interface', 'job'],
                group=GroupLeft(),
            ),
            '''
                foo * on(
                    interface, job
                ) group_left bar
            ''',
        )

        self._assert_pretty_equal(
            BinOp(
                '*',
                Metric('foo'),
                Metric('bar'),
                on=['interface', 'job'],
                group=GroupLeft('node', 'resource'),
            ),
            '''
                foo * on(
                    interface, job
                ) group_left(
                    node, resource
                ) bar
            ''',
        )
