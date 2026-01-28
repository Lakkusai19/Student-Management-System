from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'employee_id', 'attendance', 'grade')
    list_filter = ('role',)
    search_fields = ('user__username', 'employee_id')