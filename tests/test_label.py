from unittest import TestCase

from pangolier.metrics import Metric
from pangolier.label import Label


class TestLabel(TestCase):
    def test_simple_label(self) -> None:
        self.assertEqual(
            Metric('http_requests_total').where(
                Label('job') == 'prometheus',
                Label('group') == 'canary',
            ).to_str(),
            'http_requests_total{job="prometheus", group="canary"}'
        )
