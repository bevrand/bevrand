import json

from api.tests.base import BaseTestCase


def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in str for c in set]

class TestRandomizerService(BaseTestCase):
    """Tests for the Randomize Service."""

    def test_viewisup(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert containsAny('pong', data['message'])
        assert containsAny('success', data['status'])