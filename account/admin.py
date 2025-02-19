from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import User, TempUser, UserDistrictPermissions
from django import forms

# Register your models here.


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['id','email', 'name', 'department', 'mobilenumber', 'distinations', 'user_department', 'is_active', 'is_admin', 'created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'department', 'tc', 'distinations', 'user_department',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'user_permissions')}),
        ('Important Dates', {'fields': ('created_at', 'updated_at')}),
    )

    readonly_fields = ('created_at', 'updated_at')

    list_filter = ['is_active', 'is_admin']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'department', 'mobilenumber', 'distinations', 'user_department', 'tc', 'password1', 'password2', 'user_permissions'),
        }),
    )

    search_fields = ('email', 'name','mobilenumber')
    filter_horizontal = ('user_permissions',)


    # Custom action to update is_active field
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected users have been activated.")

    make_active.short_description = "Activate selected users"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been deactivated.")

    make_inactive.short_description = "Deactivate selected users"

    actions = [make_active, make_inactive]

admin.site.register(User, UserAdmin)


@admin.register(TempUser)
class TempUserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'created_at']
    search_fields = ['phone','created_at']
    list_filter = ('created_at',)


class UserDistrictPermissionsForm(forms.ModelForm):
    user_id = forms.IntegerField(label='User ID')

    class Meta:
        model = UserDistrictPermissions
        fields = ['user_id', 'district', 'status']

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        if not User.objects.filter(id=user_id).exists():
            raise forms.ValidationError("User with this ID does not exist.")
        return user_id

    def save(self, commit=True):
        instance = super().save(commit=False)
        user_id = self.cleaned_data.get('user_id')
        instance.user = User.objects.get(id=user_id)  # Set the user field with the User instance
        if commit:
            instance.save()
        return instance

class UserDistrictPermissionsAdmin(admin.ModelAdmin):
    form = UserDistrictPermissionsForm
    list_display = ('user', 'district', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'district')
    search_fields = ('user__email', 'district__DISTRICT_N')

admin.site.register(UserDistrictPermissions, UserDistrictPermissionsAdmin)