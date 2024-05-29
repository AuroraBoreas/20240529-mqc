import datetime
import typing
import faker, random

from django.core.management.base import BaseCommand

from core.user.models import AppUser
from core.mqc.models import (
    Department,
    ResponsibilityCategory,
    PartCategory,
    Location,
    DivisionCategory,
    MajorQualityCase,
)

P = typing.ParamSpec('P')

class Command(BaseCommand):
    help = 'Populate a simple table with sample data'

    def handle(self, *args: P.args, **kwargs: P.kwargs) -> None:
        fake = faker.Faker()
        n = 10
        departments = []
        for _ in range(n):
            departments.append(Department.objects.get_or_create(
                name=fake.word(),
            )[0])
        responsibilityCategories = []
        for _ in range(n):
            responsibilityCategories.append(ResponsibilityCategory.objects.get_or_create(
                name=fake.word(),
            )[0])
        partCategories = []
        for _ in range(n):
            partCategories.append(PartCategory.objects.get_or_create(
                name=fake.word(),
            )[0])
        divisionCategories = []
        for e in ['HES', 'Imaging']:
            divisionCategories.append(
                DivisionCategory.objects.get_or_create(name=e)
            [0])
        users = AppUser.objects.all()
        booleans = [True, False]
        locations = [
            Location.objects.get_or_create(name=e)[0]
            for e in ['QC', '製造', '市場', 'Other']
        ]
        n = 1_000
        for _ in range(n):
            MajorQualityCase.objects.create(
                進捗=random.randint(0,100),
                市場発生=random.choice(booleans),
                再発防止=random.choice(booleans),
                出荷停止=random.choice(booleans),
                責区=random.choice(responsibilityCategories),
                責任者=random.choice(users),
                TAT=random.randint(1,100),
                製品分=random.choice(partCategories),
                分類=random.choice(divisionCategories),
                案件名=fake.sentence(random.randint(4,10)),
                機種名型番=fake.lexify(text='???').upper() + fake.numerify(text='##'),
                進捗状況=fake.paragraph(),
                発生場所=random.choice(locations),
                発生日=fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                不良症状内容=fake.sentence(random.randint(4,10)),
                保留対象=random.randint(1,10_000),
                依頼日=fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                停止日=fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                解除日=fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                単品在庫=random.randint(1,10_000),
                半製品在庫=random.randint(1,10_000),
                完成品在庫=random.randint(1,10_000),
                外部在庫=random.randint(1,10_000),
                対応内容=fake.paragraph(),
                実施予定日=fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                実施実際日=fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                実施部署=random.choice(departments),
                実施者=random.choice(users),
                発生原因=fake.paragraph(),
                流出原因 =fake.paragraph(),
                なぜなぜ =fake.paragraph(),
                分析完了予定日 =fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                分析完了実際日 =fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                是正処置発生対策 =fake.paragraph(),
                是正処置流出対策 =fake.paragraph(),
                是正処置再発防止 =fake.paragraph(),
                是正完了予定日 =fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                是正完了実際日 =fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31)),
                CLOSE日 =fake.date_between(datetime.date(2000,1,1), datetime.date(2024,12,31))
            )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
