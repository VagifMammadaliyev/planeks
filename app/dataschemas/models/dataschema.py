from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

__all__ = ["DataSchema"]


class DataSchema(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dataschemas",
        related_query_name="dataschema",
    )

    title = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "user"], name="unique_title_for_user"
            )
        ]

    def __str__(self):
        return self.title

    @cached_property
    def data_columns(self):
        return list(self.columns.order_by("order"))

    def get_head_row(self):
        return [column.title for column in self.data_columns]

    def generate_row(self):
        return [column.generate_value() for column in self.data_columns]

    def generate_rows(self, count, include_header=True):
        if include_header:
            yield self.get_head_row()
        for i in range(count):
            yield self.generate_row()
