import factory
from .models import AppUser

class AppUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AppUser
    username = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')