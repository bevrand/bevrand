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
    def test_get_all_users(self):
        """Ensure get all users behaves correctly."""
        with self.client:
            response = self.client.get(f'/api/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            length_of_list = data['users'].__len__()
            self.assertTrue(length_of_list > 1)
            self.assertTrue('thomas' in data['users'])
            self.assertTrue('beveragerandomizer' in data['users'])


    def test_get_single_user(self):
        """Ensure get specific user behaves correctly."""
        response = self.client.get(f'/api/users')
        users = json.loads(response.data.decode())
        userlist = users['users']
        for user in userlist:
            with self.client:
                response = self.client.get(f'/api/users&user={user}')
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 200)
                length_of_list = data['descriptions'].__len__()
                self.assertTrue(length_of_list > 0)

    def test_get_beverages_specific_user(self):
        """Ensure get specific beverage based on a list and user behaves correctly."""
        response = self.client.get(f'/api/users')
        users = json.loads(response.data.decode())
        userlist = users['users']
        for user in userlist:
            response = self.client.get(f'/api/users&user={user}')
            data = json.loads(response.data.decode())
            descriptions = data['descriptions']
            for desc in descriptions:
                with self.client:
                    response = self.client.get(f'/api/users?user={user}&list={desc}')
                    data = json.loads(response.data.decode())
                    self.assertEqual(response.status_code, 200)
                    length_of_list = data['beverages'].__len__()
                    self.assertTrue(length_of_list > 0)
