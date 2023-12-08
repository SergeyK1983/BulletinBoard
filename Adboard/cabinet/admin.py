from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'photo')
    list_display_links = ('username',)
    search_fields = ('username', 'first_name')
    list_filter = ('is_superuser', 'is_staff')


admin.site.register(User, UserAdmin)
