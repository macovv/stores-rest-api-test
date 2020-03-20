from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))

    def register_and_login(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           header={'Content-Type': 'application/json'})
                self.assertIs('accesss_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
