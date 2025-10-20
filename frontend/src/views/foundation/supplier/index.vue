<template>
  <div class="supplier-container">
    <!-- 搜索栏 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="供应商编码">
          <el-input v-model="searchForm.supplier_code" placeholder="请输入供应商编码" clearable />
        </el-form-item>
        <el-form-item label="供应商名称">
          <el-input v-model="searchForm.supplier_name" placeholder="请输入供应商名称" clearable />
        </el-form-item>
        <el-form-item label="供应商类型">
          <el-select v-model="searchForm.supplier_type" placeholder="请选择供应商类型" clearable>
            <el-option label="生产商" :value="1" />
            <el-option label="经销商" :value="2" />
            <el-option label="代理商" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="供应商等级">
          <el-select v-model="searchForm.supplier_level" placeholder="请选择供应商等级" clearable>
            <el-option label="A级" :value="1" />
            <el-option label="B级" :value="2" />
            <el-option label="C级" :value="3" />
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

    <!-- 表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>供应商列表</span>
          <el-button type="primary" @click="handleAdd">新增供应商</el-button>
        </div>
      </template>

      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="supplier_code" label="供应商编码" width="150" />
        <el-table-column prop="supplier_name" label="供应商名称" width="200" />
        <el-table-column prop="supplier_type" label="供应商类型" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.supplier_type === 1" type="primary">生产商</el-tag>
            <el-tag v-else-if="row.supplier_type === 2" type="success">经销商</el-tag>
            <el-tag v-else-if="row.supplier_type === 3" type="warning">代理商</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="supplier_level" label="供应商等级" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.supplier_level === 1" type="danger">A级</el-tag>
            <el-tag v-else-if="row.supplier_level === 2" type="warning">B级</el-tag>
            <el-tag v-else-if="row.supplier_level === 3" type="info">C级</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="contact_person" label="联系人" width="120" />
        <el-table-column prop="contact_phone" label="联系电话" width="150" />
        <el-table-column prop="contact_email" label="联系邮箱" width="200" />
        <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
        <el-table-column prop="payment_days" label="付款账期(天)" width="120" />
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

      <!-- 分页 -->
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

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="供应商编码" prop="supplier_code">
              <el-input v-model="form.supplier_code" placeholder="请输入供应商编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="供应商名称" prop="supplier_name">
              <el-input v-model="form.supplier_name" placeholder="请输入供应商名称" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="供应商类型" prop="supplier_type">
              <el-select v-model="form.supplier_type" placeholder="请选择供应商类型" style="width: 100%">
                <el-option label="生产商" :value="1" />
                <el-option label="经销商" :value="2" />
                <el-option label="代理商" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="供应商等级" prop="supplier_level">
              <el-select v-model="form.supplier_level" placeholder="请选择供应商等级" style="width: 100%">
                <el-option label="A级" :value="1" />
                <el-option label="B级" :value="2" />
                <el-option label="C级" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系人" prop="contact_person">
              <el-input v-model="form.contact_person" placeholder="请输入联系人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contact_phone">
              <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系邮箱" prop="contact_email">
              <el-input v-model="form.contact_email" placeholder="请输入联系邮箱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="付款账期(天)" prop="payment_days">
              <el-input-number v-model="form.payment_days" :min="0" :max="365" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="详细地址" prop="address">
              <el-input v-model="form.address" placeholder="请输入详细地址" />
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
              <el-input
                v-model="form.remark"
                type="textarea"
                :rows="3"
                placeholder="请输入备注"
              />
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
import {
  getSupplierList,
  createSupplier,
  updateSupplier,
  deleteSupplier
} from '@/api/supplier'

// 搜索表单
const searchForm = reactive({
  supplier_code: '',
  supplier_name: '',
  supplier_type: null,
  supplier_level: null,
  status: null
})

// 表格数据
const tableData = ref([])
const loading = ref(false)

// 分页
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增供应商')
const formRef = ref(null)

// 表单数据
const form = reactive({
  id: null,
  supplier_code: '',
  supplier_name: '',
  supplier_type: 1,
  supplier_level: 2,
  contact_person: '',
  contact_phone: '',
  contact_email: '',
  address: '',
  payment_days: 0,
  status: 1,
  remark: ''
})

// 表单验证规则
const rules = {
  supplier_code: [
    { required: true, message: '请输入供应商编码', trigger: 'blur' }
  ],
  supplier_name: [
    { required: true, message: '请输入供应商名称', trigger: 'blur' }
  ],
  supplier_type: [
    { required: true, message: '请选择供应商类型', trigger: 'change' }
  ],
  supplier_level: [
    { required: true, message: '请选择供应商等级', trigger: 'change' }
  ],
  contact_phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  contact_email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 获取供应商列表
const fetchSupplierList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...searchForm
    }
    const response = await getSupplierList(params)
    console.log('Supplier list response:', response)

    if (response.code === 200) {
      tableData.value = response.data.results || []
      pagination.total = response.data.count || 0
    } else {
      ElMessage.error(response.message || '获取供应商列表失败')
    }
  } catch (error) {
    console.error('Failed to fetch supplier list:', error)
    ElMessage.error('获取供应商列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchSupplierList()
}

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    supplier_code: '',
    supplier_name: '',
    supplier_type: null,
    supplier_level: null,
    status: null
  })
  pagination.page = 1
  fetchSupplierList()
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增供应商'
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑供应商'
  Object.assign(form, {
    id: row.id,
    supplier_code: row.supplier_code,
    supplier_name: row.supplier_name,
    supplier_type: row.supplier_type,
    supplier_level: row.supplier_level,
    contact_person: row.contact_person || '',
    contact_phone: row.contact_phone || '',
    contact_email: row.contact_email || '',
    address: row.address || '',
    payment_days: row.payment_days || 0,
    status: row.status,
    remark: row.remark || ''
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除供应商"${row.supplier_name}"吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await deleteSupplier(row.id)
    console.log('Delete response:', response)

    if (response.code === 200) {
      ElMessage.success('删除成功')
      fetchSupplierList()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete supplier:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    const data = { ...form }
    delete data.id

    let response
    if (form.id) {
      response = await updateSupplier(form.id, data)
    } else {
      response = await createSupplier(data)
    }

    console.log('Submit response:', response)

    if (response.code === 200 || response.code === 201) {
      ElMessage.success(form.id ? '更新成功' : '创建成功')
      dialogVisible.value = false
      fetchSupplierList()
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

// 对话框关闭
const handleDialogClose = () => {
  formRef.value?.resetFields()
  Object.assign(form, {
    id: null,
    supplier_code: '',
    supplier_name: '',
    supplier_type: 1,
    supplier_level: 2,
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    address: '',
    payment_days: 0,
    status: 1,
    remark: ''
  })
}

// 分页
const handleSizeChange = (size) => {
  pagination.page_size = size
  fetchSupplierList()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchSupplierList()
}

// 初始化
onMounted(() => {
  fetchSupplierList()
})
</script>

<style scoped>
.supplier-container {
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
