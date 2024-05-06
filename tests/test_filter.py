from unittest import TestCase

from pangolier.metrics import Metric
from pangolier.filters import NotEqualFilter, RegexpFilter, NotRegexpFilter


class TestFilter(TestCase):
    def test_simple_filter(self) -> None:
        self.assertEqual(
            Metric('http_requests_total').filter(
                job='prometheus',
                group='canary'
            ).to_str(),
            'http_requests_total{job="prometheus", group="canary"}'
        )

    def test_chain_filter(self) -> None:
        self.assertEqual(
            Metric('http_requests_total').filter(
                job='prometheus',
            ).filter(
                group='canary'
            ).to_str(),
            'http_requests_total{job="prometheus", group="canary"}'
        )

    def test_filter_will_not_modify_origin_metric(self) -> None:
        m = Metric('http_requests_total').filter(
            job='prometheus',
        )

        self.assertEqual(
            m.to_str(),
            'http_requests_total{job="prometheus"}'
        )
        self.assertEqual(
            m.filter(
                group='canary'
            ).to_str(),
            'http_requests_total{job="prometheus", group="canary"}'
        )
        self.assertEqual(
            m.to_str(),
            'http_requests_total{job="prometheus"}'
        )

    def test_regexp_filter(self) -> None:
        self.assertEqual(
            Metric('http_requests_total').filter(
                job=RegexpFilter('prometheus-.*'),
            ).to_str(),
            'http_requests_total{job=~"prometheus-.*"}'
        )

    def test_not_equal_filter(self) -> None:
        self.assertEqual(
            Metric('http_requests_total').filter(
                job=NotEqualFilter(''),
            ).to_str(),
            'http_requests_total{job!=""}'
        )

    def test_not_regexp_filter(self) -> None:
        self.assertEqual(
            Metric('http_requests_total').filter(
                job=NotRegexpFilter('prometheus-.*'),
            ).to_str(),
            'http_requests_total{job!~"prometheus-.*"}'
        )
