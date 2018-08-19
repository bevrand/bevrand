from api.tests.base import BaseTestCase
import json


class TestController(BaseTestCase):
    """Tests for the Playlist Controller."""

    def test_view_is_up(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/api/v1/private/ping')
        data = json.loads(response.data.decode())
        assert 200 == 200

