from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_ser(self):
        user = UserModel('test', 'abcdd')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')