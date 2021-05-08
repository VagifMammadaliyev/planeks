from tests.base_classes import TestCase
from tests.factories.dataschema_factories import DataSchemaFactory
from dataschemas.models import DataSet


class DataSetManagerTestCase(TestCase):
    def test_simple(self):
        schema = DataSchemaFactory()
        dataset = DataSet.objects.create_from_dataschema(schema, 445)
        self.assertEqual(dataset.schema, schema)
        self.assertEqual(dataset.row_count, 445)
