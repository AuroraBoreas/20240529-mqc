import typing
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import AppUser

P = typing.ParamSpec('P')

@receiver(signals.post_save, sender=AppUser)
def assign_group_permission(
    sender: AppUser,
    instance: AppUser,
    created: bool,
    **kwargs: P.kwargs
) -> typing.Any:
    if created:
        try:
            group = Group.objects.get(name='mqc_perms')
            instance.groups.add(group)
        except Group.DoesNotExist:
            return