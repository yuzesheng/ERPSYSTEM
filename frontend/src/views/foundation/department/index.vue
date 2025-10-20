<template>
  <div class="department-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>部门管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增部门
          </el-button>
        </div>
      </template>

      <div class="search-bar">
        <el-input
          v-model="searchText"
          placeholder="请输入部门名称或编码"
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

      <el-table
        ref="tableRef"
        :data="tableData"
        row-key="id"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        border
        stripe
        v-loading="loading"
      >
        <el-table-column prop="name" label="部门名称" min-width="200" />
        <el-table-column prop="code" label="部门编码" width="150" />
        <el-table-column prop="manager_name" label="负责人" width="120" />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="sort_order" label="排序" width="80" align="center" />
        <el-table-column prop="is_active" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
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
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="上级部门">
          <el-tree-select
            v-model="form.parent"
            :data="treeData"
            :props="{ label: 'name', value: 'id' }"
            clearable
            placeholder="请选择上级部门(不选则为顶级部门)"
            check-strictly
            :render-after-expand="false"
          />
        </el-form-item>
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="部门编码" prop="code">
          <el-input v-model="form.code" placeholder="请输入部门编码" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" :max="9999" />
        </el-form-item>
        <el-form-item label="部门描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入部门描述"
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import {
  getDepartmentList,
  getDepartmentTree,
  createDepartment,
  updateDepartment,
  deleteDepartment
} from '@/api/department'

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
  name: '',
  code: '',
  description: '',
  sort_order: 0,
  is_active: true
})

const rules = {
  name: [
    { required: true, message: '请输入部门名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入部门编码', trigger: 'blur' }
  ],
  sort_order: [
    { required: true, message: '请输入排序', trigger: 'blur' }
  ]
}

// 加载部门列表
const loadData = async () => {
  loading.value = true
  try {
    const res = await getDepartmentTree()
    tableData.value = res.data
    // 构建树形选择器数据
    treeData.value = buildTreeSelectData(res.data)
  } catch (error) {
    ElMessage.error('加载部门数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 构建树形选择器数据
const buildTreeSelectData = (data, excludeId = null) => {
  return data.filter(item => item.id !== excludeId).map(item => ({
    id: item.id,
    name: item.name,
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
  dialogTitle.value = '新增部门'
  resetForm()
  dialogVisible.value = true
}

// 添加下级
const handleAddChild = (row) => {
  isEdit.value = false
  dialogTitle.value = '新增下级部门'
  resetForm()
  form.parent = row.id
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑部门'
  Object.assign(form, {
    id: row.id,
    parent: row.parent,
    name: row.name,
    code: row.code,
    description: row.description,
    sort_order: row.sort_order,
    is_active: row.is_active
  })
  // 重新构建树形选择器数据,排除当前编辑的部门
  treeData.value = buildTreeSelectData(tableData.value, row.id)
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除部门"${row.name}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const res = await deleteDepartment(row.id)
      console.log('删除响应:', res)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error('删除错误:', error)
      console.error('删除错误详情:', error.response?.data)
      const errorMsg = error.response?.data?.message || error.message || '删除失败'
      ElMessage.error(errorMsg)
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
        console.log('提交的数据:', data)
        if (isEdit.value) {
          const res = await updateDepartment(data.id, data)
          console.log('更新响应:', res)
          ElMessage.success('编辑成功')
        } else {
          const res = await createDepartment(data)
          console.log('创建响应:', res)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        loadData()
      } catch (error) {
        console.error('提交错误:', error)
        console.error('错误详情:', error.response?.data)
        const errorMsg = error.response?.data?.message || error.message || (isEdit.value ? '编辑失败' : '新增失败')
        ElMessage.error(errorMsg)
        // 如果有具体的字段错误，也显示出来
        if (error.response?.data?.data) {
          console.error('字段错误:', error.response.data.data)
        }
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
    name: '',
    code: '',
    description: '',
    sort_order: 0,
    is_active: true
  })
  treeData.value = buildTreeSelectData(tableData.value)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.department-container {
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
