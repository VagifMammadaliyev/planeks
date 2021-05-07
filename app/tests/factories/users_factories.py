import factory
from factory.django import DjangoModelFactory

from users import models as um


class UserFactory(DjangoModelFactory):
    class Meta:
        model = um.User

    first_name = "first_name"
    last_name = "last_name"
    email = factory.Faker("ascii_email")
    is_active = True
    is_superuser = False
    is_staff = False
