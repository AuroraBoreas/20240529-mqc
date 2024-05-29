from django.contrib import admin
from .models import MailingGroup

# Register your models here.
class MailingGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)  # Display members as a horizontal filter

admin.site.register(MailingGroup, MailingGroupAdmin)