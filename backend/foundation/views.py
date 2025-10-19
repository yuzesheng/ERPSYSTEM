from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import Department, User, Role, Permission, Menu
from .serializers import (
    DepartmentSerializer, UserListSerializer, UserDetailSerializer,
    UserCreateSerializer, UserUpdateSerializer, RoleSerializer,
    PermissionSerializer, MenuSerializer, MenuTreeSerializer,
    UserProfileSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """自定义JWT登录视图"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'code': 400,
                'message': '用户名和密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                'code': 401,
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({
                'code': 403,
                'message': '用户已被禁用'
            }, status=status.HTTP_403_FORBIDDEN)

        # 更新最后登录信息
        user.last_login = timezone.now()
        user.last_login_ip = self.get_client_ip(request)
        user.save(update_fields=['last_login', 'last_login_ip'])

        # 生成token
        refresh = RefreshToken.for_user(user)

        # 获取用户信息
        user_data = UserProfileSerializer(user).data

        return Response({
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user_data
            }
        })

    def get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class CustomTokenRefreshView(TokenRefreshView):
    """自定义Token刷新视图"""
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """用户登出"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        return Response({
            'code': 200,
            'message': '登出成功'
        })
    except Exception as e:
        return Response({
            'code': 400,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """获取当前用户信息"""
    serializer = UserProfileSerializer(request.user)
    return Response({
        'code': 200,
        'message': '获取成功',
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_menus(request):
    """获取当前用户的菜单"""
    user = request.user

    # 如果是超级管理员,返回所有菜单
    if user.is_superuser:
        menus = Menu.objects.filter(is_visible=True).order_by('sort_order')
    else:
        # 获取用户所有角色的权限
        permission_codes = set()
        for role in user.roles.filter(is_active=True):
            for perm in role.permissions.all():
                permission_codes.add(perm.code)

        # 获取有权限的菜单
        menus = Menu.objects.filter(
            is_visible=True,
            permission__code__in=permission_codes
        ).order_by('sort_order')

    # 构建树形菜单
    menu_tree = []
    menu_dict = {}

    for menu in menus:
        menu_data = {
            'id': menu.id,
            'name': menu.name,
            'title': menu.title,
            'path': menu.path,
            'component': menu.component,
            'icon': menu.icon,
            'menu_type': menu.menu_type,
            'parent_id': menu.parent_id,
            'sort_order': menu.sort_order,
            'is_cache': menu.is_cache,
            'is_external': menu.is_external,
            'children': []
        }
        menu_dict[menu.id] = menu_data

    # 构建树形结构
    for menu_id, menu_data in menu_dict.items():
        if menu_data['parent_id'] is None:
            menu_tree.append(menu_data)
        else:
            parent = menu_dict.get(menu_data['parent_id'])
            if parent:
                parent['children'].append(menu_data)

    return Response({
        'code': 200,
        'message': '获取成功',
        'data': menu_tree
    })


class DepartmentViewSet(viewsets.ModelViewSet):
    """部门管理视图集"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取部门树"""
        departments = Department.objects.filter(parent__isnull=True)
        tree_data = self._build_tree(departments)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': tree_data
        })

    def _build_tree(self, departments):
        """递归构建树形结构"""
        tree = []
        for dept in departments:
            node = {
                'id': dept.id,
                'name': dept.name,
                'code': dept.code,
                'manager_name': dept.manager.username if dept.manager else None,
                'is_active': dept.is_active,
                'children': self._build_tree(dept.get_children())
            }
            tree.append(node)
        return tree


class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserDetailSerializer

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """重置用户密码"""
        user = self.get_object()
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({
                'code': 400,
                'message': '新密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({
            'code': 200,
            'message': '密码重置成功'
        })


class RoleViewSet(viewsets.ModelViewSet):
    """角色管理视图集"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def destroy(self, request, *args, **kwargs):
        """删除角色"""
        instance = self.get_object()

        if instance.is_system:
            return Response({
                'code': 400,
                'message': '系统角色不能删除'
            }, status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)


class PermissionViewSet(viewsets.ModelViewSet):
    """权限管理视图集"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class MenuViewSet(viewsets.ModelViewSet):
    """菜单管理视图集"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取菜单树"""
        menus = Menu.objects.filter(parent__isnull=True).order_by('sort_order')
        serializer = MenuTreeSerializer(menus, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
