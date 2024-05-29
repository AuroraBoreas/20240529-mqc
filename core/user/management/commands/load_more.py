import typing
P = typing.ParamSpec('P')

from django.core.management.base import BaseCommand
from core.user.factories import AppUserFactory

class Command(BaseCommand):
    help = 'Generate test data using FactoryBoy'

    def add_arguments(self, parser) -> None:
        parser.add_argument('count', type=int, help='Number of test data instances to create')

    def handle(self, *args: P.args, **options: P.kwargs) -> None:
        self.stdout.write(self.style.NOTICE('Start generating test data..'))
        count = options['count']
        if count <= 0:
            self.stdout.write(self.style.WARNING('Count must be a positive integer'))
            return
        for _ in range(count):
            AppUserFactory.create()
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} instances of {AppUserFactory._meta.model.__name__}'))
