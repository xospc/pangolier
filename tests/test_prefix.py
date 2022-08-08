from unittest import TestCase

from pangolier.prefixes import MetricPrefix


class TestPrefix(TestCase):
    def test_add_suffix(self):
        self.assertEqual(
            MetricPrefix('http_requests').add_suffix('_total').to_str(),
            'http_requests_total'
        )

    def test_after_filter(self):
        self.assertEqual(
            MetricPrefix(
                'http_requests'
            ).filter(
                job='prometheus',
            ).filter(
                group='canary'
            ).add_suffix(
                '_total'
            ).to_str(),
            'http_requests_total{job="prometheus", group="canary"}'
        )
