from django.contrib import admin
from .models import AppUser

class AppUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', ]
    filter_horizontal = ['groups', 'user_permissions', ]
    fieldsets = (
        (None, {
            "fields": (
                'username', 'email',
            ),
        }),
        ('Permissions', {
            "fields": (
                'groups', 'user_permissions',
            ),
        }),
    )
    # add_fieldsets = (
    # )
    search_fields = ('username', 'email',)
    ordering = ('-date_joined', )

admin.site.register(AppUser, AppUserAdmin)