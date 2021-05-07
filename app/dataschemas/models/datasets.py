from django.db import models


__all__ = ["DataSet"]


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
