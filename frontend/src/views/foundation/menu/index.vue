<template>
  <div class="menu-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>菜单管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增菜单
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchText"
          placeholder="请输入菜单名称"
          clearable
          style="width: 300px"
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button @click="expandAll">展开全部</el-button>
        <el-button @click="collapseAll">收起全部</el-button>
      </div>

      <!-- 菜单树形表格 -->
      <el-table
        ref="tableRef"
        :data="tableData"
        row-key="id"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        border
        stripe
        v-loading="loading"
      >
        <el-table-column prop="title" label="菜单名称" min-width="200" />
        <el-table-column prop="name" label="路由名称" width="150" />
        <el-table-column prop="path" label="路由路径" width="180" />
        <el-table-column prop="component" label="组件路径" min-width="200" show-overflow-tooltip />
        <el-table-column prop="icon" label="图标" width="100" align="center">
          <template #default="{ row }">
            <el-icon v-if="row.icon">
              <component :is="row.icon" />
            </el-icon>
          </template>
        </el-table-column>
        <el-table-column prop="menu_type" label="菜单类型" width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.menu_type === 'menu'" type="primary" size="small">菜单</el-tag>
            <el-tag v-else-if="row.menu_type === 'button'" type="success" size="small">按钮</el-tag>
            <el-tag v-else type="info" size="small">目录</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="80" align="center" />
        <el-table-column prop="is_visible" label="可见" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_visible ? 'success' : 'danger'" size="small">
              {{ row.is_visible ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="success" size="small" link @click="handleAddChild(row)">
              添加下级
            </el-button>
            <el-button type="danger" size="small" link @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="700px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="上级菜单">
              <el-tree-select
                v-model="form.parent"
                :data="treeData"
                :props="{ label: 'title', value: 'id' }"
                clearable
                placeholder="请选择上级菜单(不选则为顶级菜单)"
                check-strictly
                :render-after-expand="false"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜单类型" prop="menu_type">
              <el-radio-group v-model="form.menu_type">
                <el-radio label="directory">目录</el-radio>
                <el-radio label="menu">菜单</el-radio>
                <el-radio label="button">按钮</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="菜单名称" prop="title">
              <el-input v-model="form.title" placeholder="请输入菜单名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="路由名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入路由名称" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20" v-if="form.menu_type !== 'button'">
          <el-col :span="12">
            <el-form-item label="路由路径" prop="path">
              <el-input v-model="form.path" placeholder="请输入路由路径" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="组件路径" v-if="form.menu_type === 'menu'">
              <el-input v-model="form.component" placeholder="如: views/user/index" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="菜单图标">
              <el-input v-model="form.icon" placeholder="请输入图标名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="排序" prop="sort_order">
              <el-input-number v-model="form.sort_order" :min="0" :max="9999" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="是否可见">
              <el-switch v-model="form.is_visible" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否缓存">
              <el-switch v-model="form.is_cache" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="外部链接">
          <el-switch v-model="form.is_external" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import {
  getMenuTree,
  createMenu,
  updateMenu,
  deleteMenu
} from '@/api/menu'

const tableRef = ref(null)
const formRef = ref(null)
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const searchText = ref('')
const tableData = ref([])
const treeData = ref([])
const isEdit = ref(false)

const form = reactive({
  id: null,
  parent: null,
  title: '',
  name: '',
  path: '',
  component: '',
  icon: '',
  menu_type: 'menu',
  sort_order: 0,
  is_visible: true,
  is_cache: false,
  is_external: false
})

const rules = {
  title: [
    { required: true, message: '请输入菜单名称', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入路由名称', trigger: 'blur' }
  ],
  path: [
    { required: true, message: '请输入路由路径', trigger: 'blur' }
  ],
  menu_type: [
    { required: true, message: '请选择菜单类型', trigger: 'change' }
  ],
  sort_order: [
    { required: true, message: '请输入排序', trigger: 'blur' }
  ]
}

// 加载菜单树
const loadData = async () => {
  loading.value = true
  try {
    const res = await getMenuTree()
    tableData.value = res.data
    treeData.value = buildTreeSelectData(res.data)
  } catch (error) {
    ElMessage.error('加载菜单数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 构建树形选择器数据
const buildTreeSelectData = (data, excludeId = null) => {
  return data.filter(item => item.id !== excludeId).map(item => ({
    id: item.id,
    title: item.title,
    children: item.children ? buildTreeSelectData(item.children, excludeId) : []
  }))
}

// 搜索
const handleSearch = () => {
  // TODO: 实现搜索逻辑
  console.log('搜索:', searchText.value)
}

// 展开全部
const expandAll = () => {
  toggleExpand(tableData.value, true)
}

// 收起全部
const collapseAll = () => {
  toggleExpand(tableData.value, false)
}

// 切换展开/收起
const toggleExpand = (data, isExpand) => {
  data.forEach(item => {
    tableRef.value.toggleRowExpansion(item, isExpand)
    if (item.children && item.children.length > 0) {
      toggleExpand(item.children, isExpand)
    }
  })
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增菜单'
  resetForm()
  dialogVisible.value = true
}

// 添加下级
const handleAddChild = (row) => {
  isEdit.value = false
  dialogTitle.value = '新增下级菜单'
  resetForm()
  form.parent = row.id
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑菜单'
  Object.assign(form, {
    id: row.id,
    parent: row.parent,
    title: row.title,
    name: row.name,
    path: row.path,
    component: row.component,
    icon: row.icon,
    menu_type: row.menu_type,
    sort_order: row.sort_order,
    is_visible: row.is_visible,
    is_cache: row.is_cache,
    is_external: row.is_external
  })
  // 重新构建树形选择器数据,排除当前编辑的菜单
  treeData.value = buildTreeSelectData(tableData.value, row.id)
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除菜单"${row.title}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteMenu(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      const errorMsg = error.response?.data?.message || '删除失败'
      ElMessage.error(errorMsg)
      console.error(error)
    }
  }).catch(() => {})
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const data = { ...form }
        if (isEdit.value) {
          await updateMenu(data.id, data)
          ElMessage.success('编辑成功')
        } else {
          await createMenu(data)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        loadData()
      } catch (error) {
        const errorMsg = error.response?.data?.message || (isEdit.value ? '编辑失败' : '新增失败')
        ElMessage.error(errorMsg)
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

// 关闭对话框
const handleDialogClose = () => {
  resetForm()
  formRef.value?.clearValidate()
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    id: null,
    parent: null,
    title: '',
    name: '',
    path: '',
    component: '',
    icon: '',
    menu_type: 'menu',
    sort_order: 0,
    is_visible: true,
    is_cache: false,
    is_external: false
  })
  treeData.value = buildTreeSelectData(tableData.value)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.menu-container {
  width: 100%;
  height: 100%;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .search-bar {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
  }
}
</style>
