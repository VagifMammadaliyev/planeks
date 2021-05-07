import random

from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.functional import cached_property
from faker import Faker

__all__ = ["DataColumn"]


class DataColumn(models.Model):
    DEFAULT_RANGE_FROM = 0
    DEFAULT_RANGE_TO = 10

    FULL_NAME_DATA_TYPE = "fn"
    JOB_DATA_TYPE = "jb"
    EMAIL_DATA_TYPE = "em"
    DOMAIN_DATA_TYPE = "do"
    PHONE_NUMBER_DATA_TYPE = "pn"
    COMPANY_NAME_DATA_TYPE = "cn"
    TEXT_DATA_TYPE = "te"
    INTEGER_DATA_TYPE = "in"
    ADDRESS_DATA_TYPE = "ad"
    DATE_DATA_TYPE = "da"
    DATA_TYPES = (
        (FULL_NAME_DATA_TYPE, "Full name"),
        (JOB_DATA_TYPE, "Job title"),
        (EMAIL_DATA_TYPE, "Email address"),
        (DOMAIN_DATA_TYPE, "Domain name"),
        (PHONE_NUMBER_DATA_TYPE, "Phone number"),
        (COMPANY_NAME_DATA_TYPE, "Company name"),
        (TEXT_DATA_TYPE, "Text"),
        (INTEGER_DATA_TYPE, "Integer number"),
        (ADDRESS_DATA_TYPE, "Address"),
        (DATE_DATA_TYPE, "Date"),
    )
    FLAT_DATA_TYPES = [dt_choice[0] for dt_choice in DATA_TYPES]
    RANGE_REQUIRED_DATA_TYPES = (INTEGER_DATA_TYPE, TEXT_DATA_TYPE)

    schema = models.ForeignKey(
        "dataschemas.DataSchema",
        on_delete=models.CASCADE,
        related_name="columns",
        related_query_name="column",
    )

    title = models.CharField(max_length=255)
    data_type = models.CharField(max_length=2, choices=DATA_TYPES)
    range_from = models.IntegerField(null=True, blank=True)
    range_to = models.IntegerField(null=True, blank=True)

    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "schema"], name="unique_column_for_schema"
            )
        ]

    def __str__(self):
        return self.title

    @classmethod
    def is_range_required(cls, data_type):
        if data_type not in cls.FLAT_DATA_TYPES:
            raise ValueError(f"'{data_type}' is not a valid data type.")
        return data_type in cls.RANGE_REQUIRED_DATA_TYPES

    @property
    def is_range_defined(self):
        return self.range_from and self.range_to

    @cached_property
    def _fake(self):
        Faker.seed(timezone.now().timestamp())
        fake = Faker()
        return fake

    def _generate_random_full_name(self):
        return self._fake.name()

    def _generate_random_job_title(self):
        return self._fake.job()

    def _generate_random_domain(self):
        return self._fake.domain_name()

    def _generate_random_email(self):
        return self._fake.email()

    def _generate_random_phone_number(self):
        return self._fake.phone_number()

    def _generate_random_compnay_name(self):
        return self._fake.company()

    def _generate_random_address(self):
        return self._fake.address()

    def _generate_random_date(self):
        return self._fake.date()

    def _generate_random_integer_value(self, range_from, range_to):
        return random.randint(range_from, range_to)

    def _generate_random_text_value(self, min_sentences, max_sentences):
        nb_sentences = self._generate_random_integer_value(min_sentences, max_sentences)
        text = [
            self._fake.sentence(self._generate_random_integer_value(3, 6))
            for _ in range(nb_sentences)
        ]
        return " ".join(text)

    def _generated_non_ranged_value(self):
        if self.data_type == self.FULL_NAME_DATA_TYPE:
            return self._generate_random_full_name()
        elif self.data_type == self.JOB_DATA_TYPE:
            return self._generate_random_job_title()
        elif self.data_type == self.EMAIL_DATA_TYPE:
            return self._generate_random_email()
        elif self.data_type == self.DOMAIN_DATA_TYPE:
            return self._generate_random_domain()
        elif self.data_type == self.PHONE_NUMBER_DATA_TYPE:
            return self._generate_random_phone_number()
        elif self.data_type == self.COMPANY_NAME_DATA_TYPE:
            return self._generate_random_compnay_name()
        elif self.data_type == self.ADDRESS_DATA_TYPE:
            return self._generate_random_address()
        elif self.data_type == self.DATE_DATA_TYPE:
            return self._generate_random_date()

    def _generate_ranged_value(self):
        # this method only called when self.is_range_required is True
        range_from = self.DEFAULT_RANGE_FROM
        range_to = self.DEFAULT_RANGE_TO
        if self.is_range_defined:
            range_from = self.range_from
            range_to = self.range_to

        if self.data_type == self.INTEGER_DATA_TYPE:
            return self._generate_random_integer_value(range_from, range_to)
        elif self.data_type == self.TEXT_DATA_TYPE:
            return self._generate_random_text_value(range_from, range_to)

    def generate_value(self):
        is_range_required = DataColumn.is_range_required(self.data_type)
        if is_range_required:
            return self._generate_ranged_value()
        return self._generated_non_ranged_value()

    def clean(self):
        if DataColumn.is_range_required(self.data_type) and not self.is_range_defined:
            range_is_required = "Range is required for selected data type"
            raise ValidationError(
                {"range_from": range_is_required, "range_to": range_is_required}
            )
        elif not DataColumn.is_range_required(self.data_type) and self.is_range_defined:
            range_is_not_required = "Range is not required for selected data type"
            raise ValidationError(
                {"range_from": range_is_not_required, "range_to": range_is_not_required}
            )

        if self.is_range_defined and self.range_from == self.range_to:
            range_from_is_same_as_range_to = "Range from cannot be same as range to"
            raise ValidationError(
                {
                    "range_from": range_from_is_same_as_range_to,
                    "range_to": range_from_is_same_as_range_to,
                }
            )
        if self.is_range_defined and self.range_from > self.range_to:
            range_from_must_be_less_than_range_to = (
                "Range from must be less than range to"
            )
            raise ValidationError({"range_from": range_from_must_be_less_than_range_to})
