from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin): # type: ignore
    list_display = ('email', 'username',
                    'first_name', 'last_name',)
    list_filter = ('email', 'username')
