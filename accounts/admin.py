from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['last_name', 'first_name', 'username', 'email', 'role', 'course', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ("School Profile", {'fields': ('role', 'course')}),
    )
