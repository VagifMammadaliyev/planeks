from django.test import (
    LiveServerTestCase as BaseLiveServerTestCase,
    SimpleTestCase as BaseSimpleTestCase,
    TestCase as BaseTestCase,
    TransactionTestCase as BaseTransactionTestCase,
)


class TestMixin:
    """
    Whenever we want to add some base functionality
    to all test cases we will define our methods here.
    """


class SimpleTestCase(TestMixin, BaseSimpleTestCase):
    pass


class TransactionTestCase(TestMixin, BaseTransactionTestCase):
    pass


class TestCase(TestMixin, BaseTestCase):
    pass


class LiveServerTestCase(TestMixin, BaseLiveServerTestCase):
    pass
