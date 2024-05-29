import contextlib
import string
import typing
import faker, random

from django.core.management.base import BaseCommand
from core.user.models import AppUser

P = typing.ParamSpec('P')

@contextlib.contextmanager
def random_state(seed: int | None) -> typing.Generator[None,None,None]:
    state = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(state)

class Command(BaseCommand):
    help = 'Populate a simple table with sample data'

    def generate_random_password(self, length: int) -> str:
        with random_state(42):
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(length))
            return password

    def handle(self, *args: P.args, **kwargs: P.kwargs) -> None:
        fake = faker.Faker()
        n = 100
        objs = []
        for _ in range(n):
            objs.append(AppUser.objects.create(
                username=fake.name(),
                email=fake.email(),
                password=self.generate_random_password(10)
            ))
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
