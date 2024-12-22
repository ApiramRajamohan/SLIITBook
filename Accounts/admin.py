from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from .forms import UserCreationForm,UserChangeForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = Account
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ['email','username','Fname','Mname','Lname','dob','department','Address']
    list_filter = ['is_active','is_admin']

    search_fields = ['email','username']
    ordering = ['username']

    # Fields displayed on the "Add User" form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_admin', 'Fname', 'Lname', 'dob', 'department', 'Gender')
        }),
    )

    # Fields displayed on the user detail form
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('Fname', 'Lname', 'Mname', 'bio', 'Address', 'dob', 'department', 'Gender')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Account, CustomUserAdmin)
