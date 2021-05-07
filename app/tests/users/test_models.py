from tests.base_classes import TestCase
from tests.factories.users_factories import UserFactory
from users.models import User


class UserFullnameTestCase(TestCase):
    def test_simple(self):
        user = UserFactory(first_name="Anna", last_name="Weekend")
        self.assertEqual(user.full_name, "Anna Weekend")

    def test_empty_first_and_last_names(self):
        user = UserFactory(first_name="", last_name="")
        self.assertEqual(user.full_name, User.DEFAULT_FULL_NAME)

    def test_empty_first_name(self):
        user = UserFactory(first_name="")
        self.assertEqual(user.full_name, user.last_name)

    def test_empty_last_name(self):
        user = UserFactory(last_name="")
        self.assertEqual(user.full_name, user.first_name)
