# coding: utf-8
from django.core.management.base import BaseCommand
from django.db import transaction
from foundation.models import Department, Role, Permission, User


class Command(BaseCommand):
    help = '初始化基础数据（部门、角色、权限）'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始初始化基础数据...'))

        # 初始化权限
        self.init_permissions()

        # 初始化部门
        self.init_departments()

        # 初始化角色
        self.init_roles()

        self.stdout.write(self.style.SUCCESS('基础数据初始化完成！'))

    def init_permissions(self):
        """初始化权限数据"""
        self.stdout.write('正在初始化权限...')

        permissions_data = [
            # 基础数据模块权限
            {'name': '部门查看', 'code': 'foundation:department:view', 'module': 'foundation', 'description': '查看部门列表和详情'},
            {'name': '部门新增', 'code': 'foundation:department:add', 'module': 'foundation', 'description': '新增部门'},
            {'name': '部门编辑', 'code': 'foundation:department:edit', 'module': 'foundation', 'description': '编辑部门信息'},
            {'name': '部门删除', 'code': 'foundation:department:delete', 'module': 'foundation', 'description': '删除部门'},

            {'name': '用户查看', 'code': 'foundation:user:view', 'module': 'foundation', 'description': '查看用户列表和详情'},
            {'name': '用户新增', 'code': 'foundation:user:add', 'module': 'foundation', 'description': '新增用户'},
            {'name': '用户编辑', 'code': 'foundation:user:edit', 'module': 'foundation', 'description': '编辑用户信息'},
            {'name': '用户删除', 'code': 'foundation:user:delete', 'module': 'foundation', 'description': '删除用户'},
            {'name': '用户重置密码', 'code': 'foundation:user:reset_pwd', 'module': 'foundation', 'description': '重置用户密码'},

            {'name': '角色查看', 'code': 'foundation:role:view', 'module': 'foundation', 'description': '查看角色列表和详情'},
            {'name': '角色新增', 'code': 'foundation:role:add', 'module': 'foundation', 'description': '新增角色'},
            {'name': '角色编辑', 'code': 'foundation:role:edit', 'module': 'foundation', 'description': '编辑角色信息'},
            {'name': '角色删除', 'code': 'foundation:role:delete', 'module': 'foundation', 'description': '删除角色'},

            {'name': '菜单查看', 'code': 'foundation:menu:view', 'module': 'foundation', 'description': '查看菜单列表和详情'},
            {'name': '菜单新增', 'code': 'foundation:menu:add', 'module': 'foundation', 'description': '新增菜单'},
            {'name': '菜单编辑', 'code': 'foundation:menu:edit', 'module': 'foundation', 'description': '编辑菜单信息'},
            {'name': '菜单删除', 'code': 'foundation:menu:delete', 'module': 'foundation', 'description': '删除菜单'},

            {'name': '客户查看', 'code': 'foundation:customer:view', 'module': 'foundation', 'description': '查看客户列表和详情'},
            {'name': '客户新增', 'code': 'foundation:customer:add', 'module': 'foundation', 'description': '新增客户'},
            {'name': '客户编辑', 'code': 'foundation:customer:edit', 'module': 'foundation', 'description': '编辑客户信息'},
            {'name': '客户删除', 'code': 'foundation:customer:delete', 'module': 'foundation', 'description': '删除客户'},

            {'name': '供应商查看', 'code': 'foundation:supplier:view', 'module': 'foundation', 'description': '查看供应商列表和详情'},
            {'name': '供应商新增', 'code': 'foundation:supplier:add', 'module': 'foundation', 'description': '新增供应商'},
            {'name': '供应商编辑', 'code': 'foundation:supplier:edit', 'module': 'foundation', 'description': '编辑供应商信息'},
            {'name': '供应商删除', 'code': 'foundation:supplier:delete', 'module': 'foundation', 'description': '删除供应商'},

            # 库存管理模块权限
            {'name': '物料分类查看', 'code': 'inventory:category:view', 'module': 'inventory', 'description': '查看物料分类列表和详情'},
            {'name': '物料分类新增', 'code': 'inventory:category:add', 'module': 'inventory', 'description': '新增物料分类'},
            {'name': '物料分类编辑', 'code': 'inventory:category:edit', 'module': 'inventory', 'description': '编辑物料分类信息'},
            {'name': '物料分类删除', 'code': 'inventory:category:delete', 'module': 'inventory', 'description': '删除物料分类'},

            {'name': '物料查看', 'code': 'inventory:material:view', 'module': 'inventory', 'description': '查看物料列表和详情'},
            {'name': '物料新增', 'code': 'inventory:material:add', 'module': 'inventory', 'description': '新增物料'},
            {'name': '物料编辑', 'code': 'inventory:material:edit', 'module': 'inventory', 'description': '编辑物料信息'},
            {'name': '物料删除', 'code': 'inventory:material:delete', 'module': 'inventory', 'description': '删除物料'},

            {'name': '仓库查看', 'code': 'inventory:warehouse:view', 'module': 'inventory', 'description': '查看仓库列表和详情'},
            {'name': '仓库新增', 'code': 'inventory:warehouse:add', 'module': 'inventory', 'description': '新增仓库'},
            {'name': '仓库编辑', 'code': 'inventory:warehouse:edit', 'module': 'inventory', 'description': '编辑仓库信息'},
            {'name': '仓库删除', 'code': 'inventory:warehouse:delete', 'module': 'inventory', 'description': '删除仓库'},

            # 销售管理模块权限
            {'name': '销售订单查看', 'code': 'sales:order:view', 'module': 'sales', 'description': '查看销售订单列表和详情'},
            {'name': '销售订单新增', 'code': 'sales:order:add', 'module': 'sales', 'description': '新增销售订单'},
            {'name': '销售订单编辑', 'code': 'sales:order:edit', 'module': 'sales', 'description': '编辑销售订单'},
            {'name': '销售订单删除', 'code': 'sales:order:delete', 'module': 'sales', 'description': '删除销售订单'},
            {'name': '销售订单审核', 'code': 'sales:order:audit', 'module': 'sales', 'description': '审核销售订单'},

            # 采购管理模块权限
            {'name': '采购订单查看', 'code': 'purchase:order:view', 'module': 'purchase', 'description': '查看采购订单列表和详情'},
            {'name': '采购订单新增', 'code': 'purchase:order:add', 'module': 'purchase', 'description': '新增采购订单'},
            {'name': '采购订单编辑', 'code': 'purchase:order:edit', 'module': 'purchase', 'description': '编辑采购订单'},
            {'name': '采购订单删除', 'code': 'purchase:order:delete', 'module': 'purchase', 'description': '删除采购订单'},
            {'name': '采购订单审核', 'code': 'purchase:order:audit', 'module': 'purchase', 'description': '审核采购订单'},

            # 生产管理模块权限
            {'name': '生产订单查看', 'code': 'production:order:view', 'module': 'production', 'description': '查看生产订单列表和详情'},
            {'name': '生产订单新增', 'code': 'production:order:add', 'module': 'production', 'description': '新增生产订单'},
            {'name': '生产订单编辑', 'code': 'production:order:edit', 'module': 'production', 'description': '编辑生产订单'},
            {'name': '生产订单删除', 'code': 'production:order:delete', 'module': 'production', 'description': '删除生产订单'},

            # 财务管理模块权限
            {'name': '应收账款查看', 'code': 'finance:receivable:view', 'module': 'finance', 'description': '查看应收账款'},
            {'name': '应付账款查看', 'code': 'finance:payable:view', 'module': 'finance', 'description': '查看应付账款'},

            # 人力资源模块权限
            {'name': '员工信息查看', 'code': 'hr:employee:view', 'module': 'hr', 'description': '查看员工信息'},
            {'name': '员工信息编辑', 'code': 'hr:employee:edit', 'module': 'hr', 'description': '编辑员工信息'},

            # 物流管理模块权限
            {'name': '物流单查看', 'code': 'logistics:order:view', 'module': 'logistics', 'description': '查看物流单'},
            {'name': '物流单编辑', 'code': 'logistics:order:edit', 'module': 'logistics', 'description': '编辑物流单'},

            # 报表管理模块权限
            {'name': '销售报表查看', 'code': 'reports:sales:view', 'module': 'reports', 'description': '查看销售报表'},
            {'name': '库存报表查看', 'code': 'reports:inventory:view', 'module': 'reports', 'description': '查看库存报表'},
            {'name': '财务报表查看', 'code': 'reports:finance:view', 'module': 'reports', 'description': '查看财务报表'},
        ]

        created_count = 0
        for perm_data in permissions_data:
            perm, created = Permission.objects.get_or_create(
                code=perm_data['code'],
                defaults=perm_data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'权限初始化完成，共创建 {created_count} 条权限记录'))

    def init_departments(self):
        """初始化部门数据"""
        self.stdout.write('正在初始化部门...')

        # 清空已有部门
        Department.objects.all().delete()

        # 创建总部
        headquarters = Department.objects.create(
            name='企业集团总部',
            code='HQ',
            description='企业集团总部',
            sort_order=0,
            is_active=True
        )

        # 创建一级部门
        departments_level1 = [
            {'name': '总经理办公室', 'code': 'CEO', 'parent': headquarters, 'sort_order': 1},
            {'name': '运营中心', 'code': 'OPS', 'parent': headquarters, 'sort_order': 2},
            {'name': '研发中心', 'code': 'RD', 'parent': headquarters, 'sort_order': 3},
            {'name': '生产中心', 'code': 'PROD', 'parent': headquarters, 'sort_order': 4},
            {'name': '市场营销中心', 'code': 'MKT', 'parent': headquarters, 'sort_order': 5},
        ]

        dept_objects = {}
        for dept_data in departments_level1:
            dept = Department.objects.create(**dept_data)
            dept_objects[dept_data['code']] = dept

        # 创建二级部门
        departments_level2 = [
            # 运营中心下属部门
            {'name': '财务部', 'code': 'FIN', 'parent': dept_objects['OPS'], 'sort_order': 1},
            {'name': '人力资源部', 'code': 'HR', 'parent': dept_objects['OPS'], 'sort_order': 2},
            {'name': '行政部', 'code': 'ADM', 'parent': dept_objects['OPS'], 'sort_order': 3},
            {'name': 'IT部', 'code': 'IT', 'parent': dept_objects['OPS'], 'sort_order': 4},

            # 研发中心下属部门
            {'name': '产品设计部', 'code': 'PD', 'parent': dept_objects['RD'], 'sort_order': 1},
            {'name': '软件开发部', 'code': 'DEV', 'parent': dept_objects['RD'], 'sort_order': 2},
            {'name': '质量管理部', 'code': 'QA', 'parent': dept_objects['RD'], 'sort_order': 3},

            # 生产中心下属部门
            {'name': '生产计划部', 'code': 'PP', 'parent': dept_objects['PROD'], 'sort_order': 1},
            {'name': '生产执行部', 'code': 'PE', 'parent': dept_objects['PROD'], 'sort_order': 2},
            {'name': '仓储物流部', 'code': 'WH', 'parent': dept_objects['PROD'], 'sort_order': 3},

            # 市场营销中心下属部门
            {'name': '销售部', 'code': 'SALES', 'parent': dept_objects['MKT'], 'sort_order': 1},
            {'name': '市场部', 'code': 'MKT_SUB', 'parent': dept_objects['MKT'], 'sort_order': 2},
            {'name': '客户服务部', 'code': 'CS', 'parent': dept_objects['MKT'], 'sort_order': 3},
        ]

        for dept_data in departments_level2:
            Department.objects.create(**dept_data)

        self.stdout.write(self.style.SUCCESS(f'部门初始化完成，共创建 {1 + len(departments_level1) + len(departments_level2)} 个部门'))

    def init_roles(self):
        """初始化角色数据"""
        self.stdout.write('正在初始化角色...')

        # 获取所有权限
        all_permissions = Permission.objects.all()
        foundation_perms = Permission.objects.filter(module='foundation')
        inventory_perms = Permission.objects.filter(module='inventory')
        sales_perms = Permission.objects.filter(module='sales')
        purchase_perms = Permission.objects.filter(module='purchase')
        production_perms = Permission.objects.filter(module='production')
        finance_perms = Permission.objects.filter(module='finance')
        hr_perms = Permission.objects.filter(module='hr')
        logistics_perms = Permission.objects.filter(module='logistics')
        reports_perms = Permission.objects.filter(module='reports')

        # 定义角色数据
        roles_data = [
            {
                'name': '超级管理员',
                'code': 'super_admin',
                'description': '拥有系统所有权限',
                'is_system': True,
                'sort_order': 1,
                'permissions': all_permissions
            },
            {
                'name': '系统管理员',
                'code': 'system_admin',
                'description': '负责系统配置和基础数据管理',
                'is_system': True,
                'sort_order': 2,
                'permissions': foundation_perms
            },
            {
                'name': '总经理',
                'code': 'ceo',
                'description': '公司总经理，拥有大部分权限',
                'is_system': False,
                'sort_order': 3,
                'permissions': all_permissions
            },
            {
                'name': '部门经理',
                'code': 'dept_manager',
                'description': '部门经理，管理本部门业务',
                'is_system': False,
                'sort_order': 4,
                'permissions': list(foundation_perms.filter(code__contains=':view')) + \
                              list(inventory_perms.filter(code__contains=':view')) + \
                              list(sales_perms) + list(purchase_perms) + list(reports_perms)
            },
            {
                'name': '财务人员',
                'code': 'finance_staff',
                'description': '财务部门员工',
                'is_system': False,
                'sort_order': 5,
                'permissions': finance_perms
            },
            {
                'name': '人事专员',
                'code': 'hr_staff',
                'description': '人力资源部门员工',
                'is_system': False,
                'sort_order': 6,
                'permissions': list(hr_perms) + list(foundation_perms.filter(code__contains='user'))
            },
            {
                'name': '销售人员',
                'code': 'sales_staff',
                'description': '销售部门员工',
                'is_system': False,
                'sort_order': 7,
                'permissions': list(sales_perms) + \
                              list(foundation_perms.filter(code__contains='customer')) + \
                              list(inventory_perms.filter(code__contains=':view'))
            },
            {
                'name': '采购人员',
                'code': 'purchase_staff',
                'description': '采购部门员工',
                'is_system': False,
                'sort_order': 8,
                'permissions': list(purchase_perms) + \
                              list(foundation_perms.filter(code__contains='supplier')) + \
                              list(inventory_perms.filter(code__contains=':view'))
            },
            {
                'name': '生产人员',
                'code': 'production_staff',
                'description': '生产部门员工',
                'is_system': False,
                'sort_order': 9,
                'permissions': list(production_perms) + list(inventory_perms)
            },
            {
                'name': '研发人员',
                'code': 'rd_staff',
                'description': '研发部门员工',
                'is_system': False,
                'sort_order': 10,
                'permissions': list(inventory_perms.filter(code__contains='material'))
            },
            {
                'name': 'IT人员',
                'code': 'it_staff',
                'description': 'IT部门员工',
                'is_system': False,
                'sort_order': 11,
                'permissions': foundation_perms
            },
            {
                'name': '仓库管理员',
                'code': 'warehouse_staff',
                'description': '仓库管理员',
                'is_system': False,
                'sort_order': 12,
                'permissions': list(inventory_perms) + list(logistics_perms)
            },
            {
                'name': '普通员工',
                'code': 'staff',
                'description': '普通员工，仅查看权限',
                'is_system': False,
                'sort_order': 99,
                'permissions': list(all_permissions.filter(code__contains=':view'))
            },
        ]

        created_count = 0
        for role_data in roles_data:
            permissions = role_data.pop('permissions')
            role, created = Role.objects.get_or_create(
                code=role_data['code'],
                defaults=role_data
            )
            if created:
                created_count += 1
                # 设置权限
                role.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS(f'角色初始化完成，共创建 {created_count} 个角色'))
