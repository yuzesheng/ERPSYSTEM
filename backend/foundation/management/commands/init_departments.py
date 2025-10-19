from django.core.management.base import BaseCommand
from foundation.models import Department, User


class Command(BaseCommand):
    help = '初始化部门数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化部门数据...')

        # 清空现有部门数据
        Department.objects.all().delete()

        # 获取管理员用户
        admin = User.objects.filter(is_superuser=True).first()

        # 创建总公司
        company = Department.objects.create(
            name='企业集团总部',
            code='DEPT001',
            description='企业集团总部',
            sort_order=1,
            is_active=True,
            manager=admin
        )
        self.stdout.write(self.style.SUCCESS(f'创建部门: {company.name}'))

        # 创建一级部门
        tech_dept = Department.objects.create(
            name='技术研发中心',
            code='DEPT010',
            parent=company,
            description='负责公司产品研发和技术创新',
            sort_order=1,
            is_active=True,
            manager=admin
        )
        self.stdout.write(self.style.SUCCESS(f'创建部门: {tech_dept.name}'))

        sales_dept = Department.objects.create(
            name='销售管理中心',
            code='DEPT020',
            parent=company,
            description='负责公司产品销售和市场拓展',
            sort_order=2,
            is_active=True,
            manager=admin
        )
        self.stdout.write(self.style.SUCCESS(f'创建部门: {sales_dept.name}'))

        operations_dept = Department.objects.create(
            name='运营管理中心',
            code='DEPT030',
            parent=company,
            description='负责公司日常运营管理',
            sort_order=3,
            is_active=True,
            manager=admin
        )
        self.stdout.write(self.style.SUCCESS(f'创建部门: {operations_dept.name}'))

        finance_dept = Department.objects.create(
            name='财务管理中心',
            code='DEPT040',
            parent=company,
            description='负责公司财务管理和成本控制',
            sort_order=4,
            is_active=True,
            manager=admin
        )
        self.stdout.write(self.style.SUCCESS(f'创建部门: {finance_dept.name}'))

        hr_dept = Department.objects.create(
            name='人力资源中心',
            code='DEPT050',
            parent=company,
            description='负责公司人力资源管理',
            sort_order=5,
            is_active=True,
            manager=admin
        )
        self.stdout.write(self.style.SUCCESS(f'创建部门: {hr_dept.name}'))

        # 创建技术研发中心的二级部门
        Department.objects.create(
            name='前端开发部',
            code='DEPT011',
            parent=tech_dept,
            description='负责前端应用开发',
            sort_order=1,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 前端开发部'))

        Department.objects.create(
            name='后端开发部',
            code='DEPT012',
            parent=tech_dept,
            description='负责后端服务开发',
            sort_order=2,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 后端开发部'))

        Department.objects.create(
            name='测试部',
            code='DEPT013',
            parent=tech_dept,
            description='负责产品测试和质量保证',
            sort_order=3,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 测试部'))

        Department.objects.create(
            name='产品部',
            code='DEPT014',
            parent=tech_dept,
            description='负责产品设计和需求管理',
            sort_order=4,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 产品部'))

        # 创建销售管理中心的二级部门
        Department.objects.create(
            name='华北销售区',
            code='DEPT021',
            parent=sales_dept,
            description='负责华北地区销售',
            sort_order=1,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 华北销售区'))

        Department.objects.create(
            name='华东销售区',
            code='DEPT022',
            parent=sales_dept,
            description='负责华东地区销售',
            sort_order=2,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 华东销售区'))

        Department.objects.create(
            name='华南销售区',
            code='DEPT023',
            parent=sales_dept,
            description='负责华南地区销售',
            sort_order=3,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 华南销售区'))

        # 创建运营管理中心的二级部门
        Department.objects.create(
            name='客服部',
            code='DEPT031',
            parent=operations_dept,
            description='负责客户服务',
            sort_order=1,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 客服部'))

        Department.objects.create(
            name='行政部',
            code='DEPT032',
            parent=operations_dept,
            description='负责行政事务管理',
            sort_order=2,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 行政部'))

        # 创建财务管理中心的二级部门
        Department.objects.create(
            name='会计部',
            code='DEPT041',
            parent=finance_dept,
            description='负责会计核算',
            sort_order=1,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 会计部'))

        Department.objects.create(
            name='审计部',
            code='DEPT042',
            parent=finance_dept,
            description='负责内部审计',
            sort_order=2,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 审计部'))

        # 创建人力资源中心的二级部门
        Department.objects.create(
            name='招聘培训部',
            code='DEPT051',
            parent=hr_dept,
            description='负责人才招聘和培训',
            sort_order=1,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 招聘培训部'))

        Department.objects.create(
            name='薪酬绩效部',
            code='DEPT052',
            parent=hr_dept,
            description='负责薪酬和绩效管理',
            sort_order=2,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('创建部门: 薪酬绩效部'))

        self.stdout.write(self.style.SUCCESS('部门数据初始化完成!'))
        self.stdout.write(f'共创建 {Department.objects.count()} 个部门')
