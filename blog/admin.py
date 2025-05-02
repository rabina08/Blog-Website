from django.contrib import admin
from .models import User, BlogPost, Category
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'full_name', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('full_name',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name',)}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(BlogPost)
admin.site.register(Category)
