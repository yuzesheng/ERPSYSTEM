from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from foundation.models import User


class MaterialCategory(MPTTModel):
    """物料分类模型"""
    STATUS_CHOICES = [
        (1, '正常'),
        (0, '停用'),
    ]

    category_code = models.CharField('分类编码', max_length=50, unique=True)
    category_name = models.CharField('分类名称', max_length=100)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='上级分类'
    )
    sort_order = models.IntegerField('显示顺序', default=0)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=1)
    remark = models.CharField('备注', max_length=500, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_material_categories',
        verbose_name='创建人'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_material_categories',
        verbose_name='更新人'
    )
    is_deleted = models.BooleanField('是否删除', default=False)

    class MPTTMeta:
        order_insertion_by = ['sort_order', 'category_code']

    class Meta:
        db_table = 'foundation_material_category'
        verbose_name = '物料分类'
        verbose_name_plural = '物料分类'
        ordering = ['sort_order', 'category_code']
        indexes = [
            models.Index(fields=['category_code']),
        ]

    def __str__(self):
        return f"{self.category_code} - {self.category_name}"


class Material(models.Model):
    """物料模型"""
    MATERIAL_TYPE_CHOICES = [
        (1, '原材料'),
        (2, '半成品'),
        (3, '成品'),
    ]

    STATUS_CHOICES = [
        (1, '正常'),
        (0, '停用'),
    ]

    material_code = models.CharField('物料编码', max_length=50, unique=True)
    material_name = models.CharField('物料名称', max_length=200)
    material_spec = models.CharField('物料规格', max_length=200, blank=True)
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='materials',
        verbose_name='分类'
    )
    material_type = models.IntegerField('物料类型', choices=MATERIAL_TYPE_CHOICES, default=1)
    unit = models.CharField('基本单位', max_length=20, blank=True)
    price = models.DecimalField('参考价格', max_digits=18, decimal_places=2, default=0)
    min_stock = models.DecimalField('最小库存', max_digits=18, decimal_places=4, default=0)
    max_stock = models.DecimalField('最大库存', max_digits=18, decimal_places=4, default=0)
    safety_stock = models.DecimalField('安全库存', max_digits=18, decimal_places=4, default=0)
    barcode = models.CharField('条形码', max_length=100, blank=True)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=1)
    remark = models.CharField('备注', max_length=500, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_materials',
        verbose_name='创建人'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_materials',
        verbose_name='更新人'
    )
    is_deleted = models.BooleanField('是否删除', default=False)

    class Meta:
        db_table = 'foundation_material'
        verbose_name = '物料'
        verbose_name_plural = '物料'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['material_code']),
            models.Index(fields=['material_name']),
            models.Index(fields=['barcode']),
        ]

    def __str__(self):
        return f"{self.material_code} - {self.material_name}"


class Warehouse(models.Model):
    """仓库模型"""
    WAREHOUSE_TYPE_CHOICES = [
        (1, '原材料仓'),
        (2, '半成品仓'),
        (3, '成品仓'),
        (4, '综合仓'),
    ]

    STATUS_CHOICES = [
        (1, '正常'),
        (0, '停用'),
    ]

    warehouse_code = models.CharField('仓库编码', max_length=50, unique=True)
    warehouse_name = models.CharField('仓库名称', max_length=200)
    warehouse_type = models.IntegerField('仓库类型', choices=WAREHOUSE_TYPE_CHOICES, default=4)
    location = models.CharField('仓库位置', max_length=500, blank=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_warehouses',
        verbose_name='仓库管理员'
    )
    contact_phone = models.CharField('联系电话', max_length=20, blank=True)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=1)
    remark = models.CharField('备注', max_length=500, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_warehouses',
        verbose_name='创建人'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_warehouses',
        verbose_name='更新人'
    )
    is_deleted = models.BooleanField('是否删除', default=False)

    class Meta:
        db_table = 'foundation_warehouse'
        verbose_name = '仓库'
        verbose_name_plural = '仓库'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['warehouse_code']),
            models.Index(fields=['warehouse_name']),
        ]

    def __str__(self):
        return f"{self.warehouse_code} - {self.warehouse_name}"
