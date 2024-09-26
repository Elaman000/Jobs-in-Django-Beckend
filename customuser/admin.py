from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'gender', 'nationality', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gender','birth_date','nationality','applicant',       'experience','relocation','education','schedule','team','name_activity','activity','description','photo','number_persons','address','telegram','web_url','whatsapp','phone')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
