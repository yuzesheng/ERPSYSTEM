from django.db import models
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    """部门模型"""
    name = models.CharField('部门名称', max_length=100)
    code = models.CharField('部门编码', max_length=50, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='上级部门'
    )
    manager = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        verbose_name='部门负责人'
    )
    description = models.TextField('部门描述', blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['sort_order', 'code']

    class Meta:
        db_table = 'sys_department'
        verbose_name = '部门'
        verbose_name_plural = '部门'
        ordering = ['sort_order', 'code']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """用户模型 - 扩展Django自带用户模型"""
    employee_no = models.CharField('工号', max_length=50, unique=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='部门'
    )
    position = models.CharField('职位', max_length=100, blank=True)
    gender = models.CharField(
        '性别',
        max_length=10,
        choices=[('male', '男'), ('female', '女'), ('other', '其他')],
        default='other'
    )
    birthday = models.DateField('出生日期', null=True, blank=True)
    entry_date = models.DateField('入职日期', null=True, blank=True)
    status = models.CharField(
        '状态',
        max_length=20,
        choices=[
            ('active', '在职'),
            ('inactive', '离职'),
            ('suspended', '停职')
        ],
        default='active'
    )
    roles = models.ManyToManyField(
        'Role',
        related_name='users',
        verbose_name='角色',
        blank=True
    )
    last_login_ip = models.GenericIPAddressField('最后登录IP', null=True, blank=True)
    remark = models.TextField('备注', blank=True)

    # 重写groups和user_permissions,避免与Django默认User冲突
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='foundation_user_set',
        related_query_name='foundation_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='foundation_user_set',
        related_query_name='foundation_user',
    )

    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.employee_no})"


class Role(models.Model):
    """角色模型"""
    name = models.CharField('角色名称', max_length=100, unique=True)
    code = models.CharField('角色编码', max_length=50, unique=True)
    description = models.TextField('角色描述', blank=True)
    permissions = models.ManyToManyField(
        'Permission',
        related_name='roles',
        verbose_name='权限',
        blank=True
    )
    is_active = models.BooleanField('是否启用', default=True)
    is_system = models.BooleanField('是否系统角色', default=False, help_text='系统角色不可删除')
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'sys_role'
        verbose_name = '角色'
        verbose_name_plural = '角色'
        ordering = ['sort_order', 'code']

    def __str__(self):
        return self.name


class Permission(models.Model):
    """权限模型"""
    name = models.CharField('权限名称', max_length=100)
    code = models.CharField('权限编码', max_length=100, unique=True)
    module = models.CharField('所属模块', max_length=50)
    description = models.TextField('权限描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'sys_permission'
        verbose_name = '权限'
        verbose_name_plural = '权限'
        ordering = ['module', 'code']

    def __str__(self):
        return f"{self.module}.{self.name}"


class Menu(MPTTModel):
    """菜单模型"""
    MENU_TYPE_CHOICES = [
        ('directory', '目录'),
        ('menu', '菜单'),
        ('button', '按钮'),
    ]

    name = models.CharField('菜单名称', max_length=100)
    title = models.CharField('菜单标题', max_length=100)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父菜单'
    )
    menu_type = models.CharField('菜单类型', max_length=20, choices=MENU_TYPE_CHOICES, default='menu')
    path = models.CharField('路由路径', max_length=200, blank=True)
    component = models.CharField('组件路径', max_length=200, blank=True)
    icon = models.CharField('图标', max_length=50, blank=True)
    permission = models.ForeignKey(
        Permission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='menus',
        verbose_name='关联权限'
    )
    sort_order = models.IntegerField('排序', default=0)
    is_visible = models.BooleanField('是否可见', default=True)
    is_cache = models.BooleanField('是否缓存', default=True)
    is_external = models.BooleanField('是否外链', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    class Meta:
        db_table = 'sys_menu'
        verbose_name = '菜单'
        verbose_name_plural = '菜单'
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class Customer(models.Model):
    """客户模型"""
    CUSTOMER_TYPE_CHOICES = [
        (1, '企业'),
        (2, '个人'),
    ]

    CUSTOMER_LEVEL_CHOICES = [
        (1, '重要'),
        (2, '普通'),
        (3, '一般'),
    ]

    STATUS_CHOICES = [
        (1, '正常'),
        (0, '停用'),
    ]

    customer_code = models.CharField('客户编码', max_length=50, unique=True)
    customer_name = models.CharField('客户名称', max_length=200)
    customer_type = models.IntegerField('客户类型', choices=CUSTOMER_TYPE_CHOICES, default=1)
    customer_level = models.IntegerField('客户等级', choices=CUSTOMER_LEVEL_CHOICES, default=2)
    industry = models.CharField('所属行业', max_length=100, blank=True)
    contact_person = models.CharField('联系人', max_length=50, blank=True)
    contact_phone = models.CharField('联系电话', max_length=20, blank=True)
    contact_email = models.EmailField('联系邮箱', blank=True)
    address = models.CharField('详细地址', max_length=500, blank=True)
    credit_limit = models.DecimalField('信用额度', max_digits=18, decimal_places=2, default=0)
    credit_days = models.IntegerField('账期天数', default=0)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=1)
    remark = models.CharField('备注', max_length=500, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_customers',
        verbose_name='创建人'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_customers',
        verbose_name='更新人'
    )
    is_deleted = models.BooleanField('是否删除', default=False)

    class Meta:
        db_table = 'foundation_customer'
        verbose_name = '客户'
        verbose_name_plural = '客户'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer_code']),
            models.Index(fields=['customer_name']),
        ]

    def __str__(self):
        return f"{self.customer_code} - {self.customer_name}"
