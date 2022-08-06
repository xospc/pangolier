from unittest import TestCase

from pangolier.metrics import Metric
from pangolier.filters import RegexpFilter


class TestFilter(TestCase):
    def test_simple_filter(self):
        self.assertEqual(
            Metric('http_requests_total').filter(
                job='prometheus',
                group='canary'
            ).to_str(),
            'http_requests_total{job="prometheus", group="canary"}'
        )

    def test_chain_filter(self):
        self.assertEqual(
            Metric('http_requests_total').filter(
                job='prometheus',
            ).filter(
                group='canary'
            ).to_str(),
            'http_requests_total{job="prometheus", group="canary"}'
        )

    def test_filter_will_not_modify_origin_metric(self):
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

    def test_regexp_filter(self):
        self.assertEqual(
            Metric('http_requests_total').filter(
                job=RegexpFilter('prometheus-.*'),
            ).to_str(),
            'http_requests_total{job=~"prometheus-.*"}'
        )
