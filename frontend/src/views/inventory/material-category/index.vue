<template>
  <div class="material-category-container">
    <el-card class="search-card">
      <el-form :inline="true" class="search-form">
        <el-form-item>
          <el-input v-model="searchText" placeholder="搜索分类名称或编码" clearable @clear="fetchCategoryTree" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleExpandAll">{{ expandAll ? '收起全部' : '展开全部' }}</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>物料分类列表</span>
          <el-button type="primary" @click="handleAdd">新增分类</el-button>
        </div>
      </template>

      <el-table
        :data="tableData"
        border
        stripe
        v-loading="loading"
        row-key="id"
        :default-expand-all="expandAll"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="category_code" label="分类编码" width="150" />
        <el-table-column prop="category_name" label="分类名称" min-width="200" />
        <el-table-column prop="sort_order" label="排序" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 1" type="success">正常</el-tag>
            <el-tag v-else type="danger">停用</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" @close="handleDialogClose">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="分类编码" prop="category_code">
          <el-input v-model="form.category_code" placeholder="请输入分类编码" />
        </el-form-item>
        <el-form-item label="分类名称" prop="category_name">
          <el-input v-model="form.category_name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="上级分类" prop="parent">
          <el-tree-select
            v-model="form.parent"
            :data="treeSelectData"
            :props="{ label: 'category_name', value: 'id' }"
            check-strictly
            clearable
            placeholder="请选择上级分类"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">正常</el-radio>
            <el-radio :label="0">停用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMaterialCategoryTree, createMaterialCategory, updateMaterialCategory, deleteMaterialCategory } from '@/api/material-category'

const searchText = ref('')
const tableData = ref([])
const loading = ref(false)
const expandAll = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增分类')
const formRef = ref(null)

const form = reactive({
  id: null,
  category_code: '',
  category_name: '',
  parent: null,
  sort_order: 0,
  status: 1,
  remark: ''
})

const rules = {
  category_code: [{ required: true, message: '请输入分类编码', trigger: 'blur' }],
  category_name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }]
}

const treeSelectData = computed(() => {
  const filterTree = (data, excludeId) => {
    return data.filter(item => item.id !== excludeId).map(item => ({
      ...item,
      children: item.children ? filterTree(item.children, excludeId) : []
    }))
  }
  return form.id ? filterTree(tableData.value, form.id) : tableData.value
})

const fetchCategoryTree = async () => {
  loading.value = true
  try {
    const response = await getMaterialCategoryTree()
    if (response.code === 200) {
      tableData.value = response.data || []
    } else {
      ElMessage.error(response.message || '获取分类列表失败')
    }
  } catch (error) {
    console.error('Failed to fetch category tree:', error)
    ElMessage.error('获取分类列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  fetchCategoryTree()
}

const handleExpandAll = () => {
  expandAll.value = !expandAll.value
}

const handleAdd = () => {
  dialogTitle.value = '新增分类'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑分类'
  Object.assign(form, {
    id: row.id,
    category_code: row.category_code,
    category_name: row.category_name,
    parent: row.parent || null,
    sort_order: row.sort_order || 0,
    status: row.status,
    remark: row.remark || ''
  })
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除分类"${row.category_name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const response = await deleteMaterialCategory(row.id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      fetchCategoryTree()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete category:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    const data = { ...form }
    delete data.id
    let response
    if (form.id) {
      response = await updateMaterialCategory(form.id, data)
    } else {
      response = await createMaterialCategory(data)
    }
    if (response.code === 200 || response.code === 201) {
      ElMessage.success(form.id ? '更新成功' : '创建成功')
      dialogVisible.value = false
      fetchCategoryTree()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    console.error('Form validation or submit failed:', error)
    if (error !== false) {
      ElMessage.error('操作失败')
    }
  }
}

const handleDialogClose = () => {
  formRef.value?.resetFields()
  Object.assign(form, {
    id: null,
    category_code: '',
    category_name: '',
    parent: null,
    sort_order: 0,
    status: 1,
    remark: ''
  })
}

onMounted(() => {
  fetchCategoryTree()
})
</script>

<style scoped>
.material-category-container {
  padding: 20px;
}
.search-card {
  margin-bottom: 20px;
}
.search-form {
  display: flex;
  flex-wrap: wrap;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
