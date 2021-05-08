from django.contrib.admin.models import LogEntry

from tests.base_classes import TestCase
from tests.factories.users_factories import UserFactory
from users.models import User


class UserQuerySetFilterTestCase(TestCase):
    def test_simple_active(self):
        user = UserFactory(is_active=True)
        active_users = User.objects.all().active()
        inactive_users = User.objects.all().inactive()
        self.assertEqual(inactive_users.count(), 0)
        self.assertEqual(active_users.count(), 1)
        self.assertEqual(active_users.first().id, user.id)

    def test_simple_inactive(self):
        user = UserFactory(is_active=False)
        active_users = User.objects.all().active()
        inactive_users = User.objects.all().inactive()
        self.assertEqual(inactive_users.count(), 1)
        self.assertEqual(active_users.count(), 0)
        self.assertEqual(inactive_users.first().id, user.id)

    def test_simple_multiple(self):
        UserFactory(is_active=False)
        UserFactory(is_active=False)
        UserFactory(is_active=True)
        active_users = User.objects.all().active()
        inactive_users = User.objects.all().inactive()
        self.assertEqual(inactive_users.count(), 2)
        self.assertEqual(active_users.count(), 1)


class UserQuerySetActionTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = UserFactory()
        cls.admin_user_id = cls.admin_user.id

    def _get_logs_count(self, **kwargs):
        return LogEntry.objects.filter(**kwargs).count()

    def _get_users(self):
        return User.objects.exclude(id=self.admin_user_id)

    def test_deactivate_fail(self):
        user = UserFactory(is_active=False)
        count = self._get_users().active().deactivate(self.admin_user_id)
        self.assertEqual(count, 0)
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        logs_count = self._get_logs_count()
        self.assertEqual(logs_count, 0)

    def test_deactivate_fail_2(self):
        user = UserFactory(is_active=False)
        count = self._get_users().inactive().deactivate(self.admin_user_id)
        self.assertEqual(
            count,
            1,
            "deactivate method must not care about incorrectly filtered queryset",
        )
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        logs_count = self._get_logs_count()
        self.assertEqual(logs_count, 1)

    def test_deactivate_success(self):
        user = UserFactory(is_active=True)
        count = self._get_users().active().deactivate(self.admin_user_id)
        self.assertEqual(count, 1)
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        logs_count = self._get_logs_count()
        self.assertEqual(logs_count, 1)

    def test_activate_fail(self):
        user = UserFactory(is_active=True)
        count = self._get_users().inactive().activate(self.admin_user_id)
        self.assertEqual(count, 0)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        logs_count = self._get_logs_count()
        self.assertEqual(logs_count, 0)

    def test_activate_fail_2(self):
        user = UserFactory(is_active=True)
        count = self._get_users().active().activate(self.admin_user_id)
        self.assertEqual(
            count,
            1,
            "activate method must not care about incorrectly filtered queryset",
        )
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        logs_count = self._get_logs_count()
        self.assertEqual(logs_count, 1)

    def test_activate_success(self):
        user = UserFactory(is_active=False)
        count = self._get_users().inactive().activate(self.admin_user_id)
        self.assertEqual(count, 1)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        logs_count = self._get_logs_count()
        self.assertEqual(logs_count, 1)
