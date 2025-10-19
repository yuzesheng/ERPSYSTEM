from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from mptt.admin import MPTTModelAdmin
from .models import Department, User, Role, Permission, Menu


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    list_display = ['name', 'code', 'manager', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    mptt_level_indent = 20


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'employee_no', 'email', 'phone', 'department', 'position', 'status', 'is_active']
    list_filter = ['status', 'is_active', 'is_staff', 'is_superuser', 'department']
    search_fields = ['username', 'employee_no', 'email', 'phone', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {
            'fields': ('employee_no', 'phone', 'avatar', 'department', 'position',
                      'gender', 'birthday', 'entry_date', 'status', 'roles',
                      'last_login_ip', 'remark')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('扩展信息', {
            'fields': ('employee_no', 'phone', 'department', 'position', 'status')
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'is_system', 'sort_order', 'created_at']
    list_filter = ['is_active', 'is_system', 'created_at']
    search_fields = ['name', 'code']
    filter_horizontal = ['permissions']
    ordering = ['sort_order', 'code']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'module', 'created_at']
    list_filter = ['module', 'created_at']
    search_fields = ['name', 'code', 'module']
    ordering = ['module', 'code']


@admin.register(Menu)
class MenuAdmin(MPTTModelAdmin):
    list_display = ['title', 'name', 'menu_type', 'path', 'icon', 'sort_order', 'is_visible']
    list_filter = ['menu_type', 'is_visible', 'is_cache']
    search_fields = ['title', 'name', 'path']
    mptt_level_indent = 20
    ordering = ['sort_order']
