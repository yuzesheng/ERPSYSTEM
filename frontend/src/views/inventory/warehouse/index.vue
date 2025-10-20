<template>
  <div class="warehouse-container">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="仓库编码">
          <el-input v-model="searchForm.warehouse_code" placeholder="请输入仓库编码" clearable />
        </el-form-item>
        <el-form-item label="仓库名称">
          <el-input v-model="searchForm.warehouse_name" placeholder="请输入仓库名称" clearable />
        </el-form-item>
        <el-form-item label="仓库类型">
          <el-select v-model="searchForm.warehouse_type" placeholder="请选择仓库类型" clearable>
            <el-option label="原材料仓" :value="1" />
            <el-option label="半成品仓" :value="2" />
            <el-option label="成品仓" :value="3" />
            <el-option label="综合仓" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="正常" :value="1" />
            <el-option label="停用" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>仓库列表</span>
          <el-button type="primary" @click="handleAdd">新增仓库</el-button>
        </div>
      </template>

      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="warehouse_code" label="仓库编码" width="150" />
        <el-table-column prop="warehouse_name" label="仓库名称" width="200" />
        <el-table-column prop="warehouse_type" label="仓库类型" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.warehouse_type === 1" type="primary">原材料仓</el-tag>
            <el-tag v-else-if="row.warehouse_type === 2" type="warning">半成品仓</el-tag>
            <el-tag v-else-if="row.warehouse_type === 3" type="success">成品仓</el-tag>
            <el-tag v-else-if="row.warehouse_type === 4" type="info">综合仓</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="仓库位置" min-width="200" show-overflow-tooltip />
        <el-table-column prop="manager_name" label="管理员" width="120" />
        <el-table-column prop="contact_phone" label="联系电话" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 1" type="success">正常</el-tag>
            <el-tag v-else type="danger">停用</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px" @close="handleDialogClose">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="仓库编码" prop="warehouse_code">
              <el-input v-model="form.warehouse_code" placeholder="请输入仓库编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="仓库名称" prop="warehouse_name">
              <el-input v-model="form.warehouse_name" placeholder="请输入仓库名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="仓库类型" prop="warehouse_type">
              <el-select v-model="form.warehouse_type" placeholder="请选择仓库类型" style="width: 100%">
                <el-option label="原材料仓" :value="1" />
                <el-option label="半成品仓" :value="2" />
                <el-option label="成品仓" :value="3" />
                <el-option label="综合仓" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contact_phone">
              <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="仓库位置" prop="location">
              <el-input v-model="form.location" placeholder="请输入仓库位置" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio :label="1">正常</el-radio>
                <el-radio :label="0">停用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注" />
            </el-form-item>
          </el-col>
        </el-row>
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getWarehouseList, createWarehouse, updateWarehouse, deleteWarehouse } from '@/api/warehouse'

const searchForm = reactive({
  warehouse_code: '',
  warehouse_name: '',
  warehouse_type: null,
  status: null
})

const tableData = ref([])
const loading = ref(false)

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const dialogVisible = ref(false)
const dialogTitle = ref('新增仓库')
const formRef = ref(null)

const form = reactive({
  id: null,
  warehouse_code: '',
  warehouse_name: '',
  warehouse_type: 4,
  location: '',
  manager: null,
  contact_phone: '',
  status: 1,
  remark: ''
})

const rules = {
  warehouse_code: [{ required: true, message: '请输入仓库编码', trigger: 'blur' }],
  warehouse_name: [{ required: true, message: '请输入仓库名称', trigger: 'blur' }],
  warehouse_type: [{ required: true, message: '请选择仓库类型', trigger: 'change' }],
  contact_phone: [{ pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }]
}

const fetchWarehouseList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...searchForm
    }
    const response = await getWarehouseList(params)
    if (response.code === 200) {
      tableData.value = response.data.results || []
      pagination.total = response.data.count || 0
    } else {
      ElMessage.error(response.message || '获取仓库列表失败')
    }
  } catch (error) {
    console.error('Failed to fetch warehouse list:', error)
    ElMessage.error('获取仓库列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchWarehouseList()
}

const handleReset = () => {
  Object.assign(searchForm, {
    warehouse_code: '',
    warehouse_name: '',
    warehouse_type: null,
    status: null
  })
  pagination.page = 1
  fetchWarehouseList()
}

const handleAdd = () => {
  dialogTitle.value = '新增仓库'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑仓库'
  Object.assign(form, {
    id: row.id,
    warehouse_code: row.warehouse_code,
    warehouse_name: row.warehouse_name,
    warehouse_type: row.warehouse_type,
    location: row.location || '',
    manager: row.manager || null,
    contact_phone: row.contact_phone || '',
    status: row.status,
    remark: row.remark || ''
  })
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除仓库"${row.warehouse_name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const response = await deleteWarehouse(row.id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      fetchWarehouseList()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete warehouse:', error)
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
      response = await updateWarehouse(form.id, data)
    } else {
      response = await createWarehouse(data)
    }
    if (response.code === 200 || response.code === 201) {
      ElMessage.success(form.id ? '更新成功' : '创建成功')
      dialogVisible.value = false
      fetchWarehouseList()
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
    warehouse_code: '',
    warehouse_name: '',
    warehouse_type: 4,
    location: '',
    manager: null,
    contact_phone: '',
    status: 1,
    remark: ''
  })
}

const handleSizeChange = (size) => {
  pagination.page_size = size
  fetchWarehouseList()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchWarehouseList()
}

onMounted(() => {
  fetchWarehouseList()
})
</script>

<style scoped>
.warehouse-container {
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
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
