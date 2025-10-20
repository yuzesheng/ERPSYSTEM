from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView, CustomTokenRefreshView,
    logout, get_user_info, get_user_menus,
    DepartmentViewSet, UserViewSet, RoleViewSet,
    PermissionViewSet, MenuViewSet, CustomerViewSet
)

# 创建路由器
router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('users', UserViewSet)
router.register('roles', RoleViewSet)
router.register('permissions', PermissionViewSet)
router.register('menus', MenuViewSet)
router.register('customers', CustomerViewSet)

urlpatterns = [
    # 认证相关
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout, name='logout'),
    path('auth/user/', get_user_info, name='user_info'),
    path('auth/menus/', get_user_menus, name='user_menus'),

    # 模块路由
    path('', include(router.urls)),
]
