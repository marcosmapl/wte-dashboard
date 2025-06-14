from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import WineUser

# Custom UserAdmin with conditional logic for superusers and staff
class WineUserAdmin(DefaultUserAdmin):
    # Customize which fields are displayed in the admin form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Login details
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),  # Personal details
        ('Roles', {'fields': ('is_admin', 'is_general_manager', 'is_operational_manager', 'is_booking_agent', 'is_read_only', 'is_it_manager')}),  # Role fields
        ('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),  # Admin permissions
    )

    # Customize fields in the user creation form (when creating a new user)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_admin')}
         ),
    )

    # Customize what fields are displayed in the list view
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_active', 'is_general_manager', 'is_operational_manager', 'is_it_manager', 'is_booking_agent', 'is_read_only'
    )

    # Filter users based on role and authorization
    list_filter = ('is_admin', 'is_general_manager', 'is_operational_manager', 'is_booking_agent', 'is_read_only', 'is_it_manager', 'is_active')

    # Customize queryset to separate superusers and staff in the admin list view
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superusers see all users
        return queryset.filter(is_superuser=False)  # Non-superuser staff won't see superusers

# Register the CustomUser model with the custom admin
admin.site.register(WineUser, WineUserAdmin)
