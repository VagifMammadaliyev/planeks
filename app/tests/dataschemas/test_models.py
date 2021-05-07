from datetime import datetime

from tests.base_classes import TestCase
from tests.factories.users_factories import UserFactory
from tests.factories.dataschema_factories import DataColumnFactory, DataSchemaFactory
from dataschemas.models import DataColumn, DataSchema


class DataColumnRangeTestCase(TestCase):
    def test_is_range_required_integer(self):
        data_column = DataColumnFactory(data_type=DataColumn.INTEGER_DATA_TYPE)
        self.assertTrue(DataColumn(data_type=data_column.data_type))

    def test_is_range_required_text(self):
        data_column = DataColumnFactory(data_type=DataColumn.TEXT_DATA_TYPE)
        self.assertTrue(DataColumn(data_type=data_column.data_type))

    def test_is_not_range_defined(self):
        data_column = DataColumnFactory()
        self.assertFalse(data_column.is_range_defined)

    def test_is_not_range_defined_2(self):
        data_column = DataColumnFactory(range_from=1)
        self.assertFalse(data_column.is_range_defined)

    def test_is_range_defined(self):
        data_column = DataColumnFactory(range_from=0, range_to=100)
        self.assertTrue(data_column.is_range_defined)

    def test_is_range_defined_2(self):
        data_column = DataColumnFactory(range_from=1, range_to=100)
        self.assertTrue(data_column.is_range_defined)


class DataColumnGenerationTestCase(TestCase):
    def assertGeneratedValueIsInstance(self, data_type, type_, **kwargs):
        data_column = DataColumnFactory(data_type=data_type, **kwargs)
        value = data_column.generate_value()
        self.assertIsInstance(value, type_)
        return value

    def test_integer_with_no_range(self):
        self.assertGeneratedValueIsInstance(DataColumn.INTEGER_DATA_TYPE, int)

    def test_integer_with_range(self):
        self.assertGeneratedValueIsInstance(
            DataColumn.INTEGER_DATA_TYPE, int, range_from=1, range_to=1000000
        )

    def test_full_name(self):
        self.assertGeneratedValueIsInstance(DataColumn.FULL_NAME_DATA_TYPE, str)

    def test_job_title(self):
        self.assertGeneratedValueIsInstance(DataColumn.JOB_DATA_TYPE, str)

    def test_email_name(self):
        email = self.assertGeneratedValueIsInstance(DataColumn.EMAIL_DATA_TYPE, str)
        self.assertIn("@", email)

    def test_domain_name(self):
        domain = self.assertGeneratedValueIsInstance(DataColumn.DOMAIN_DATA_TYPE, str)
        self.assertIn(".", domain)

    def test_phone(self):
        self.assertGeneratedValueIsInstance(DataColumn.PHONE_NUMBER_DATA_TYPE, str)

    def test_company_name(self):
        self.assertGeneratedValueIsInstance(DataColumn.COMPANY_NAME_DATA_TYPE, str)

    def test_text_data(self):
        self.assertGeneratedValueIsInstance(DataColumn.TEXT_DATA_TYPE, str)

    def test_text_data_with_2_or_3_sentences(self):
        text = self.assertGeneratedValueIsInstance(
            DataColumn.TEXT_DATA_TYPE, str, range_from=2, range_to=3
        )
        self.assertIn(text.count("."), [2, 3], text)

    def test_text_data_with_0_or_1_sentences(self):
        text = self.assertGeneratedValueIsInstance(
            DataColumn.TEXT_DATA_TYPE, str, range_from=0, range_to=1
        )
        self.assertIn(text.count("."), [0, 1], text)

    def test_addres(self):
        self.assertGeneratedValueIsInstance(DataColumn.ADDRESS_DATA_TYPE, str)

    def test_date(self):
        date = self.assertGeneratedValueIsInstance(DataColumn.DATE_DATA_TYPE, str)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            self.assertFalse(True, f"{date} is not a valid date")
