from api.tests.base import BaseTestCase
import json


class TestController(BaseTestCase):
    """Tests for the Randomize Controller."""

    def test_view_is_up(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert 'pong' in data['message']
        assert 'success' in data['status']
