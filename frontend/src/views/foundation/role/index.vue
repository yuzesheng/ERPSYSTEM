<template>
  <div class="role-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>角色管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增角色
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="角色名称">
            <el-input
              v-model="searchForm.name"
              placeholder="请输入角色名称"
              clearable
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="角色编码">
            <el-input
              v-model="searchForm.code"
              placeholder="请输入角色编码"
              clearable
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.is_active" clearable placeholder="请选择状态" style="width: 120px">
              <el-option label="启用" :value="true" />
              <el-option label="禁用" :value="false" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="handleReset">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 角色列表 -->
      <el-table
        :data="tableData"
        border
        stripe
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="name" label="角色名称" width="150" />
        <el-table-column prop="code" label="角色编码" width="150" />
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column prop="sort_order" label="排序" width="80" align="center" />
        <el-table-column prop="is_active" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_active"
              :disabled="row.is_system"
              @change="handleStatusChange(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="is_system" label="系统角色" width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.is_system" type="danger" size="small">是</el-tag>
            <el-tag v-else type="info" size="small">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="success" size="small" link @click="handleAssignPermission(row)">
              分配权限
            </el-button>
            <el-button
              type="danger"
              size="small"
              link
              :disabled="row.is_system"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadData"
          @current-change="loadData"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色编码" prop="code">
          <el-input v-model="form.code" placeholder="请输入角色编码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" :max="9999" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入角色描述"
          />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 分配权限对话框 -->
    <el-dialog
      v-model="permissionDialogVisible"
      title="分配权限"
      width="800px"
    >
      <el-form label-width="80px">
        <el-form-item label="角色名称">
          <el-tag type="primary">{{ currentRole?.name }}</el-tag>
        </el-form-item>
        <el-form-item label="权限">
          <el-tree
            ref="permissionTreeRef"
            :data="permissionTree"
            :props="{ label: 'name', children: 'children' }"
            show-checkbox
            node-key="id"
            :default-checked-keys="selectedPermissions"
            :default-expand-all="true"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handlePermissionSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import {
  getRoleList,
  createRole,
  updateRole,
  deleteRole,
  getPermissionList
} from '@/api/role'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const permissionDialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const tableData = ref([])
const permissionTree = ref([])
const selectedPermissions = ref([])
const currentRole = ref(null)
const formRef = ref(null)
const permissionTreeRef = ref(null)

// 搜索表单
const searchForm = reactive({
  name: '',
  code: '',
  is_active: null
})

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 表单
const form = reactive({
  name: '',
  code: '',
  description: '',
  sort_order: 0,
  is_active: true
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入角色编码', trigger: 'blur' },
    { pattern: /^[A-Z_]+$/, message: '角色编码只能包含大写字母和下划线', trigger: 'blur' }
  ],
  sort_order: [
    { required: true, message: '请输入排序', trigger: 'blur' }
  ]
}

// 加载权限列表
const loadPermissionList = async () => {
  try {
    const res = await getPermissionList()
    // 将权限列表转换为树形结构
    permissionTree.value = buildPermissionTree(res.data)
  } catch (error) {
    console.error('加载权限列表失败:', error)
  }
}

// 构建权限树
const buildPermissionTree = (permissions) => {
  // 按模块分组
  const modules = {}
  permissions.forEach(perm => {
    if (!modules[perm.module]) {
      modules[perm.module] = {
        id: `module_${perm.module}`,
        name: perm.module,
        children: []
      }
    }
    modules[perm.module].children.push({
      id: perm.id,
      name: perm.name,
      code: perm.code
    })
  })
  return Object.values(modules)
}

// 加载角色列表
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }
    const res = await getRoleList(params)
    if (res.data && res.data.results) {
      tableData.value = res.data.results
      pagination.total = res.data.count
    } else {
      tableData.value = res.data || []
    }
  } catch (error) {
    ElMessage.error('加载角色列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadData()
}

// 重置搜索
const handleReset = () => {
  Object.assign(searchForm, {
    name: '',
    code: '',
    is_active: null
  })
  handleSearch()
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增角色'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑角色'
  Object.assign(form, {
    id: row.id,
    name: row.name,
    code: row.code,
    description: row.description,
    sort_order: row.sort_order,
    is_active: row.is_active
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  if (row.is_system) {
    ElMessage.warning('系统角色不能删除')
    return
  }

  ElMessageBox.confirm(
    `确定要删除角色"${row.name}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteRole(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      const errorMsg = error.response?.data?.message || '删除失败'
      ElMessage.error(errorMsg)
      console.error(error)
    }
  }).catch(() => {})
}

// 状态切换
const handleStatusChange = async (row) => {
  try {
    await updateRole(row.id, { is_active: row.is_active })
    ElMessage.success('状态修改成功')
  } catch (error) {
    row.is_active = !row.is_active
    ElMessage.error('状态修改失败')
    console.error(error)
  }
}

// 分配权限
const handleAssignPermission = (row) => {
  currentRole.value = row
  selectedPermissions.value = row.permissions || []
  permissionDialogVisible.value = true
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
          await updateRole(data.id, data)
          ElMessage.success('编辑成功')
        } else {
          await createRole(data)
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

// 提交权限分配
const handlePermissionSubmit = async () => {
  if (!permissionTreeRef.value) return

  submitting.value = true
  try {
    // 获取选中的权限（包括半选中的父节点）
    const checkedKeys = permissionTreeRef.value.getCheckedKeys()
    const halfCheckedKeys = permissionTreeRef.value.getHalfCheckedKeys()

    // 过滤掉模块节点（以module_开头的）
    const permissions = [...checkedKeys, ...halfCheckedKeys].filter(id => !String(id).startsWith('module_'))

    await updateRole(currentRole.value.id, { permissions })
    ElMessage.success('权限分配成功')
    permissionDialogVisible.value = false
    loadData()
  } catch (error) {
    const errorMsg = error.response?.data?.message || '权限分配失败'
    ElMessage.error(errorMsg)
    console.error(error)
  } finally {
    submitting.value = false
  }
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
    name: '',
    code: '',
    description: '',
    sort_order: 0,
    is_active: true
  })
}

onMounted(() => {
  loadPermissionList()
  loadData()
})
</script>

<style scoped lang="scss">
.role-container {
  width: 100%;
  height: 100%;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .search-bar {
    margin-bottom: 20px;
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
