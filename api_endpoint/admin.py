from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from api_endpoint.models import User



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # model = User
    pass
