from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MaterialCategory, Material, Warehouse
from .serializers import MaterialCategorySerializer, MaterialSerializer, WarehouseSerializer


class MaterialCategoryViewSet(viewsets.ModelViewSet):
    """物料分类管理视图集"""
    queryset = MaterialCategory.objects.filter(is_deleted=False)
    serializer_class = MaterialCategorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """获取物料分类列表"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """获取物料分类详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """创建物料分类"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(created_by=request.user, updated_by=request.user)

        return Response({
            'code': 200,
            'message': '创建成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """更新物料分类"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(updated_by=request.user)

        return Response({
            'code': 200,
            'message': '更新成功',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """删除物料分类（软删除）"""
        instance = self.get_object()

        # 检查是否有子分类
        if instance.get_children().filter(is_deleted=False).exists():
            return Response({
                'code': 400,
                'message': '该分类下存在子分类，无法删除',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查是否有关联物料
        if Material.objects.filter(category=instance, is_deleted=False).exists():
            return Response({
                'code': 400,
                'message': '该分类下存在物料，无法删除',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.is_deleted = True
        instance.save()

        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取物料分类树"""
        def build_tree(parent=None):
            categories = MaterialCategory.objects.filter(parent=parent, is_deleted=False).order_by('sort_order', 'category_code')
            result = []
            for category in categories:
                serializer = self.get_serializer(category)
                item = serializer.data
                item['children'] = build_tree(category)
                result.append(item)
            return result

        tree_data = build_tree()
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': tree_data
        })


class MaterialViewSet(viewsets.ModelViewSet):
    """物料管理视图集"""
    queryset = Material.objects.filter(is_deleted=False)
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """获取物料列表"""
        queryset = self.filter_queryset(self.get_queryset())

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'results': serializer.data,
                    'count': self.paginator.page.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link()
                }
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """获取物料详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """创建物料"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(created_by=request.user, updated_by=request.user)

        return Response({
            'code': 200,
            'message': '创建成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """更新物料"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(updated_by=request.user)

        return Response({
            'code': 200,
            'message': '更新成功',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """删除物料（软删除）"""
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })


class WarehouseViewSet(viewsets.ModelViewSet):
    """仓库管理视图集"""
    queryset = Warehouse.objects.filter(is_deleted=False)
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """获取仓库列表"""
        queryset = self.filter_queryset(self.get_queryset())

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'code': 200,
                'message': '获取成功',
                'data': {
                    'results': serializer.data,
                    'count': self.paginator.page.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link()
                }
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """获取仓库详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """创建仓库"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(created_by=request.user, updated_by=request.user)

        return Response({
            'code': 200,
            'message': '创建成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """更新仓库"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(updated_by=request.user)

        return Response({
            'code': 200,
            'message': '更新成功',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """删除仓库（软删除）"""
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })
