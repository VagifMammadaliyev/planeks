import factory
from factory.django import DjangoModelFactory

from dataschemas import models as dm


class DataSchemaFactory(DjangoModelFactory):
    class Meta:
        model = dm.DataSchema

    user = factory.SubFactory("tests.factories.users_factories.UserFactory")
    title = factory.Faker("pystr", min_chars=10, max_chars=10)


class DataColumnFactory(DjangoModelFactory):
    class Meta:
        model = dm.DataColumn

    schema = factory.SubFactory(DataSchemaFactory)
    title = factory.Faker("pystr", min_chars=10, max_chars=10)
    data_type = dm.DataColumn.FULL_NAME_DATA_TYPE


class DataSetFactory(DjangoModelFactory):
    class Meta:
        model = dm.DataSet

    schema = factory.SubFactory(DataSchemaFactory)
    generated_file = factory.django.FileField(filename="generated_file_name")
    row_count = 1
