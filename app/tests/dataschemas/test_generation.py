from unittest.mock import patch

from django.utils import timezone
from tests.base_classes import TestCase
from tests.factories.dataschema_factories import DataSchemaFactory, DataSetFactory

from dataschemas.models import DataSet


class DataSetGenerationTestCase(TestCase):
    @patch("dataschemas.models.dataset.generate_csv.delay")
    def test_simple(self, mock):
        schema = DataSchemaFactory()
        dataset = DataSet.objects.create_from_dataschema(schema, 1)
        mock.assert_called()

    @patch("dataschemas.models.dataset.generate_csv.delay")
    def test_simple_skip_task(self, mock):
        schema = DataSchemaFactory()
        dataset = DataSet.objects.create_from_dataschema(schema, 1, False)
        mock.assert_not_called()

    def test_generate_creates_file(self):
        dataset = DataSetFactory(generated_file=None)
        dataset.generate()
        self.assertTrue(dataset.generated_file)

    def _create_dataset(self, generate=True):
        dataset = DataSetFactory(
            generated_file=None, started_generation_at=None, finished_generation_at=None
        )
        if generate:
            dataset.generate()
        return dataset

    def test_generate_sets_start_time(self):
        dataset = self._create_dataset()
        self.assertTrue(dataset.is_started)
        self.assertIsNotNone(dataset.started_generation_at)

    def test_generate_sets_end_time(self):
        dataset = self._create_dataset()
        self.assertTrue(dataset.is_finished)
        self.assertIsNotNone(dataset.finished_generation_at)

    def test_is_processing_logic(self):
        dataset = DataSet(
            started_generation_at=timezone.now(), finished_generation_at=None
        )
        self.assertTrue(dataset.is_processing)
