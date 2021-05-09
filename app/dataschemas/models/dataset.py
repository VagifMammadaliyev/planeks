import csv
import io
import uuid

from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from .dataschema import DataSchema
from ..tasks import generate_csv

__all__ = ["DataSet"]


class DataSetManager(models.Manager):
    def create_from_dataschema(self, dataschema, row_count, generate_file=True):
        dataset = self.create(schema=dataschema, row_count=row_count)
        if generate_file:
            generate_csv.delay(dataset.id)
        return dataset


class DataSet(models.Model):
    schema = models.ForeignKey(
        "dataschemas.DataSchema",
        on_delete=models.CASCADE,
        related_name="generations",
        related_query_name="generation",
    )

    generated_file = models.FileField(
        upload_to="generations/%Y/%m/%d/", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    started_generation_at = models.DateTimeField(null=True, blank=True)
    finished_generation_at = models.DateTimeField(null=True, blank=True)

    row_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="At least one row must be generated")]
    )
    objects = DataSetManager()

    def __str__(self):
        return f"For schema with ID={self.schema_id}"

    @property
    def is_finished(self):
        return bool(self.finished_generation_at)

    @property
    def is_started(self):
        return bool(self.started_generation_at)

    @property
    def is_processing(self):
        return self.is_started and not self.is_finished

    def _generate_file_name(self):
        return f"{self.schema.title}_{str(uuid.uuid4())}.csv"

    def aknowledge_start(self):
        self.started_generation_at = timezone.now()
        self.save(update_fields=["started_generation_at"])

    def aknowledge_completion(self):
        self.finished_generation_at = timezone.now()
        self.save(update_fields=["finished_generation_at"])

    def generate(self):
        self.aknowledge_start()
        stream = io.StringIO()
        writer = csv.writer(stream)
        for generated_row in self.schema.generate_rows(self.row_count):
            writer.writerow(generated_row)
        stream.seek(0)
        file_name = self._generate_file_name()
        self.generated_file.save(file_name, ContentFile(stream.read().encode()))
        self.aknowledge_completion()
        return (
            self.finished_generation_at - self.started_generation_at
        ).total_seconds()

    @property
    def visible_status(self):
        if self.is_finished:
            return "Finished ✅"
        else:
            return "Not ready ❌"

    @cached_property
    def elapsed_time_in_seconds(self):
        if self.is_finished:
            return (
                self.finished_generation_at - self.started_generation_at
            ).total_seconds()
        return None
