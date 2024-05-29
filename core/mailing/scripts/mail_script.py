from django.db import connection
from pprint import pprint
from core.mailing.models import MailingGroup


def run() -> None:
    objs = MailingGroup.objects.prefetch_related('members').values_list('members__email', flat=True)
    pprint(objs)
    pprint(connection.queries)
