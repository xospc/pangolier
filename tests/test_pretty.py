from textwrap import dedent
from unittest import TestCase

from pangolier.metrics import Metric


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
