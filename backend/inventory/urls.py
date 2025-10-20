from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaterialCategoryViewSet, MaterialViewSet, WarehouseViewSet

# 创建路由器
router = DefaultRouter()
router.register('material-categories', MaterialCategoryViewSet)
router.register('materials', MaterialViewSet)
router.register('warehouses', WarehouseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
