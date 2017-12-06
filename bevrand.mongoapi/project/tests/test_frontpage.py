import json
from datetime import datetime
from project.api.models import Mongoobject

from project.tests.base import BaseTestCase

def add_user(user, list):
    user = Mongoobject(user=user, list=list)
    user.dateinserted = datetime.utcnow()
    user.dateupdated = datetime.utcnow()
    user.beverages = [{"name" : "coffee", "name": " tea"}]
    return user

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_viewisup(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])


    def test_get_all_frontpage_users(self):
        """Ensure get frontpage users behaves correctly."""
        with self.client:
            response = self.client.get(f'/api/frontpage')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('TGIF' in data['front_page_lists'])
            self.assertTrue('mancavemayhem' in data['front_page_lists'])

    def test_single_frontpage_user(self):
        """Ensure get frontpage user behaves correctly."""
        response = self.client.get(f'/api/frontpage')
        frontpageusers = json.loads(response.data.decode())
        fplist = frontpageusers['front_page_lists']
        for fpuser in fplist:
            with self.client:
                response = self.client.get(f'/api/frontpage?list={fpuser}')
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 200)
                length_of_list = data['beverages'].__len__()
                self.assertTrue(length_of_list > 1)


