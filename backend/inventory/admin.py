from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import MaterialCategory, Material, Warehouse


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(MPTTModelAdmin):
    list_display = ['category_code', 'category_name', 'parent', 'sort_order', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['category_code', 'category_name']
    mptt_level_indent = 20
    ordering = ['sort_order', 'category_code']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['material_code', 'material_name', 'material_spec', 'category',
                    'material_type', 'unit', 'price', 'status', 'created_at']
    list_filter = ['material_type', 'status', 'category', 'created_at']
    search_fields = ['material_code', 'material_name', 'barcode']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['warehouse_code', 'warehouse_name', 'warehouse_type',
                    'location', 'manager', 'status', 'created_at']
    list_filter = ['warehouse_type', 'status', 'created_at']
    search_fields = ['warehouse_code', 'warehouse_name', 'location']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
