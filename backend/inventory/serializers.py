from rest_framework import serializers
from .models import MaterialCategory, Material, Warehouse


class MaterialCategorySerializer(serializers.ModelSerializer):
    """物料分类序列化器"""
    parent_name = serializers.CharField(source='parent.category_name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True, allow_null=True)

    class Meta:
        model = MaterialCategory
        fields = ['id', 'category_code', 'category_name', 'parent', 'parent_name',
                  'sort_order', 'status', 'status_display', 'remark',
                  'created_at', 'updated_at', 'created_by', 'created_by_name',
                  'updated_by', 'updated_by_name']
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
        extra_kwargs = {
            'parent': {'required': False, 'allow_null': True},
            'remark': {'required': False, 'allow_blank': True, 'allow_null': True}
        }

    def validate_category_code(self, value):
        """验证分类编码唯一性"""
        instance = self.instance
        if instance:
            if MaterialCategory.objects.exclude(pk=instance.pk).filter(category_code=value).exists():
                raise serializers.ValidationError('分类编码已存在')
        else:
            if MaterialCategory.objects.filter(category_code=value).exists():
                raise serializers.ValidationError('分类编码已存在')
        return value


class MaterialSerializer(serializers.ModelSerializer):
    """物料序列化器"""
    category_name = serializers.CharField(source='category.category_name', read_only=True, allow_null=True)
    material_type_display = serializers.CharField(source='get_material_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True, allow_null=True)

    class Meta:
        model = Material
        fields = ['id', 'material_code', 'material_name', 'material_spec',
                  'category', 'category_name', 'material_type', 'material_type_display',
                  'unit', 'price', 'min_stock', 'max_stock', 'safety_stock',
                  'barcode', 'status', 'status_display', 'remark',
                  'created_at', 'updated_at', 'created_by', 'created_by_name',
                  'updated_by', 'updated_by_name']
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
        extra_kwargs = {
            'category': {'required': False, 'allow_null': True},
            'material_spec': {'required': False, 'allow_blank': True},
            'unit': {'required': False, 'allow_blank': True},
            'barcode': {'required': False, 'allow_blank': True},
            'remark': {'required': False, 'allow_blank': True}
        }

    def validate_material_code(self, value):
        """验证物料编码唯一性"""
        instance = self.instance
        if instance:
            if Material.objects.exclude(pk=instance.pk).filter(material_code=value).exists():
                raise serializers.ValidationError('物料编码已存在')
        else:
            if Material.objects.filter(material_code=value).exists():
                raise serializers.ValidationError('物料编码已存在')
        return value


class WarehouseSerializer(serializers.ModelSerializer):
    """仓库序列化器"""
    manager_name = serializers.CharField(source='manager.username', read_only=True, allow_null=True)
    warehouse_type_display = serializers.CharField(source='get_warehouse_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True, allow_null=True)

    class Meta:
        model = Warehouse
        fields = ['id', 'warehouse_code', 'warehouse_name', 'warehouse_type',
                  'warehouse_type_display', 'location', 'manager', 'manager_name',
                  'contact_phone', 'status', 'status_display', 'remark',
                  'created_at', 'updated_at', 'created_by', 'created_by_name',
                  'updated_by', 'updated_by_name']
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
        extra_kwargs = {
            'manager': {'required': False, 'allow_null': True},
            'location': {'required': False, 'allow_blank': True},
            'contact_phone': {'required': False, 'allow_blank': True},
            'remark': {'required': False, 'allow_blank': True}
        }

    def validate_warehouse_code(self, value):
        """验证仓库编码唯一性"""
        instance = self.instance
        if instance:
            if Warehouse.objects.exclude(pk=instance.pk).filter(warehouse_code=value).exists():
                raise serializers.ValidationError('仓库编码已存在')
        else:
            if Warehouse.objects.filter(warehouse_code=value).exists():
                raise serializers.ValidationError('仓库编码已存在')
        return value
