<template>
  <div class="material-container">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="物料编码">
          <el-input v-model="searchForm.material_code" placeholder="请输入物料编码" clearable />
        </el-form-item>
        <el-form-item label="物料名称">
          <el-input v-model="searchForm.material_name" placeholder="请输入物料名称" clearable />
        </el-form-item>
        <el-form-item label="物料类型">
          <el-select v-model="searchForm.material_type" placeholder="请选择物料类型" clearable>
            <el-option label="原材料" :value="1" />
            <el-option label="半成品" :value="2" />
            <el-option label="成品" :value="3" />
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
          <span>物料列表</span>
          <el-button type="primary" @click="handleAdd">新增物料</el-button>
        </div>
      </template>

      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="material_code" label="物料编码" width="150" />
        <el-table-column prop="material_name" label="物料名称" width="200" />
        <el-table-column prop="material_spec" label="规格" width="150" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="material_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.material_type === 1" type="primary">原材料</el-tag>
            <el-tag v-else-if="row.material_type === 2" type="warning">半成品</el-tag>
            <el-tag v-else-if="row.material_type === 3" type="success">成品</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="price" label="参考价格" width="100" />
        <el-table-column prop="safety_stock" label="安全库存" width="100" />
        <el-table-column prop="status" label="状态" width="80">
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px" @close="handleDialogClose">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="物料编码" prop="material_code">
              <el-input v-model="form.material_code" placeholder="请输入物料编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="物料名称" prop="material_name">
              <el-input v-model="form.material_name" placeholder="请输入物料名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="物料规格" prop="material_spec">
              <el-input v-model="form.material_spec" placeholder="请输入物料规格" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="物料类型" prop="material_type">
              <el-select v-model="form.material_type" placeholder="请选择物料类型" style="width: 100%">
                <el-option label="原材料" :value="1" />
                <el-option label="半成品" :value="2" />
                <el-option label="成品" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="基本单位" prop="unit">
              <el-input v-model="form.unit" placeholder="请输入基本单位" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="参考价格" prop="price">
              <el-input-number v-model="form.price" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="最小库存" prop="min_stock">
              <el-input-number v-model="form.min_stock" :min="0" :precision="4" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="最大库存" prop="max_stock">
              <el-input-number v-model="form.max_stock" :min="0" :precision="4" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="安全库存" prop="safety_stock">
              <el-input-number v-model="form.safety_stock" :min="0" :precision="4" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="条形码" prop="barcode">
              <el-input v-model="form.barcode" placeholder="请输入条形码" />
            </el-form-item>
          </el-col>
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
import { getMaterialList, createMaterial, updateMaterial, deleteMaterial } from '@/api/material'

const searchForm = reactive({
  material_code: '',
  material_name: '',
  material_type: null,
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
const dialogTitle = ref('新增物料')
const formRef = ref(null)

const form = reactive({
  id: null,
  material_code: '',
  material_name: '',
  material_spec: '',
  category: null,
  material_type: 1,
  unit: '',
  price: 0,
  min_stock: 0,
  max_stock: 0,
  safety_stock: 0,
  barcode: '',
  status: 1,
  remark: ''
})

const rules = {
  material_code: [{ required: true, message: '请输入物料编码', trigger: 'blur' }],
  material_name: [{ required: true, message: '请输入物料名称', trigger: 'blur' }],
  material_type: [{ required: true, message: '请选择物料类型', trigger: 'change' }]
}

const fetchMaterialList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...searchForm
    }
    const response = await getMaterialList(params)
    if (response.code === 200) {
      tableData.value = response.data.results || []
      pagination.total = response.data.count || 0
    } else {
      ElMessage.error(response.message || '获取物料列表失败')
    }
  } catch (error) {
    console.error('Failed to fetch material list:', error)
    ElMessage.error('获取物料列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchMaterialList()
}

const handleReset = () => {
  Object.assign(searchForm, {
    material_code: '',
    material_name: '',
    material_type: null,
    status: null
  })
  pagination.page = 1
  fetchMaterialList()
}

const handleAdd = () => {
  dialogTitle.value = '新增物料'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑物料'
  Object.assign(form, {
    id: row.id,
    material_code: row.material_code,
    material_name: row.material_name,
    material_spec: row.material_spec || '',
    category: row.category || null,
    material_type: row.material_type,
    unit: row.unit || '',
    price: row.price || 0,
    min_stock: row.min_stock || 0,
    max_stock: row.max_stock || 0,
    safety_stock: row.safety_stock || 0,
    barcode: row.barcode || '',
    status: row.status,
    remark: row.remark || ''
  })
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除物料"${row.material_name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const response = await deleteMaterial(row.id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      fetchMaterialList()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete material:', error)
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
      response = await updateMaterial(form.id, data)
    } else {
      response = await createMaterial(data)
    }
    if (response.code === 200 || response.code === 201) {
      ElMessage.success(form.id ? '更新成功' : '创建成功')
      dialogVisible.value = false
      fetchMaterialList()
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
    material_code: '',
    material_name: '',
    material_spec: '',
    category: null,
    material_type: 1,
    unit: '',
    price: 0,
    min_stock: 0,
    max_stock: 0,
    safety_stock: 0,
    barcode: '',
    status: 1,
    remark: ''
  })
}

const handleSizeChange = (size) => {
  pagination.page_size = size
  fetchMaterialList()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchMaterialList()
}

onMounted(() => {
  fetchMaterialList()
})
</script>

<style scoped>
.material-container {
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
