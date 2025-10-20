from rest_framework import serializers
from .models import Department, User, Role, Permission, Menu


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器"""
    manager_name = serializers.CharField(source='manager.username', read_only=True, allow_null=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'parent', 'parent_name', 'manager',
                  'manager_name', 'description', 'sort_order', 'is_active',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'parent': {'required': False, 'allow_null': True},
            'manager': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_blank': True, 'allow_null': True}
        }


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""

    class Meta:
        model = Permission
        fields = ['id', 'name', 'code', 'module', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    permissions_detail = PermissionSerializer(source='permissions', many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'code', 'description', 'permissions', 'permissions_detail',
                  'is_active', 'is_system', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserListSerializer(serializers.ModelSerializer):
    """用户列表序列化器"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    roles_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'employee_no', 'email', 'phone', 'avatar',
                  'department', 'department_name', 'position', 'gender',
                  'status', 'roles_info', 'is_active', 'last_login', 'date_joined']

    def get_roles_info(self, obj):
        return [{'id': role.id, 'name': role.name, 'code': role.code} for role in obj.roles.all()]


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    department_info = DepartmentSerializer(source='department', read_only=True)
    roles_detail = RoleSerializer(source='roles', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'employee_no', 'email', 'phone', 'avatar',
                  'department', 'department_info', 'position', 'gender',
                  'birthday', 'entry_date', 'status', 'roles', 'roles_detail',
                  'last_login_ip', 'remark', 'is_active', 'is_staff',
                  'last_login', 'date_joined']
        read_only_fields = ['last_login', 'date_joined', 'last_login_ip']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'employee_no', 'email',
                  'phone', 'department', 'position', 'gender', 'birthday',
                  'entry_date', 'status', 'roles', 'is_active']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        roles = validated_data.pop('roles', [])

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        if roles:
            user.roles.set(roles)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""

    class Meta:
        model = User
        fields = ['employee_no', 'email', 'phone', 'avatar', 'department',
                  'position', 'gender', 'birthday', 'entry_date', 'status',
                  'roles', 'remark', 'is_active']

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if roles is not None:
            instance.roles.set(roles)

        return instance


class MenuSerializer(serializers.ModelSerializer):
    """菜单序列化器"""
    permission_info = PermissionSerializer(source='permission', read_only=True)
    parent_name = serializers.CharField(source='parent.title', read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'name', 'title', 'parent', 'parent_name', 'menu_type',
                  'path', 'component', 'icon', 'permission', 'permission_info',
                  'sort_order', 'is_visible', 'is_cache', 'is_external',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MenuTreeSerializer(serializers.ModelSerializer):
    """菜单树形序列化器"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'title', 'menu_type', 'path', 'component',
                  'icon', 'sort_order', 'is_visible', 'is_cache', 'is_external',
                  'children']

    def get_children(self, obj):
        children = obj.get_children()
        return MenuTreeSerializer(children, many=True).data


class UserProfileSerializer(serializers.ModelSerializer):
    """用户个人信息序列化器"""
    department_info = DepartmentSerializer(source='department', read_only=True)
    roles_info = serializers.SerializerMethodField()
    permissions_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'employee_no', 'email', 'phone', 'avatar',
                  'department_info', 'position', 'gender', 'birthday',
                  'entry_date', 'status', 'roles_info', 'permissions_info',
                  'last_login', 'date_joined']

    def get_roles_info(self, obj):
        return [{'id': role.id, 'name': role.name, 'code': role.code} for role in obj.roles.all()]

    def get_permissions_info(self, obj):
        permissions = set()
        for role in obj.roles.filter(is_active=True):
            for perm in role.permissions.all():
                permissions.add(perm.code)
        return list(permissions)
