<template>
  <div class="customer-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>客户管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增客户
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchForm.customer_code"
          placeholder="客户编码"
          clearable
          style="width: 200px"
        />
        <el-input
          v-model="searchForm.customer_name"
          placeholder="客户名称"
          clearable
          style="width: 200px"
        />
        <el-select
          v-model="searchForm.customer_type"
          placeholder="客户类型"
          clearable
          style="width: 150px"
        >
          <el-option label="企业" :value="1" />
          <el-option label="个人" :value="2" />
        </el-select>
        <el-select
          v-model="searchForm.customer_level"
          placeholder="客户等级"
          clearable
          style="width="150px"
        >
          <el-option label="重要" :value="1" />
          <el-option label="普通" :value="2" />
          <el-option label="一般" :value="3" />
        </el-select>
        <el-select
          v-model="searchForm.status"
          placeholder="状态"
          clearable
          style="width: 120px"
        >
          <el-option label="正常" :value="1" />
          <el-option label="停用" :value="0" />
        </el-select>
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button @click="handleReset">
          <el-icon><Refresh /></el-icon>
          重置
        </el-button>
      </div>

      <!-- 客户列表 -->
      <el-table
        :data="tableData"
        border
        stripe
        v-loading="loading"
        style="margin-top: 20px"
      >
        <el-table-column prop="customer_code" label="客户编码" width="150" />
        <el-table-column prop="customer_name" label="客户名称" min-width="180" />
        <el-table-column prop="customer_type_display" label="客户类型" width="100" align="center" />
        <el-table-column prop="customer_level_display" label="客户等级" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.customer_level === 1 ? 'danger' : row.customer_level === 2 ? 'warning' : 'info'"
              size="small"
            >
              {{ row.customer_level_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="industry" label="所属行业" width="120" show-overflow-tooltip />
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="contact_email" label="联系邮箱" width="180" show-overflow-tooltip />
        <el-table-column prop="credit_limit" label="信用额度" width="120" align="right">
          <template #default="{ row }">
            ¥{{ row.credit_limit }}
          </template>
        </el-table-column>
        <el-table-column prop="credit_days" label="账期(天)" width="100" align="center" />
        <el-table-column prop="status_display" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
              {{ row.status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" link @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 20px; justify-content: flex-end"
      />
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
        label-width="100px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户编码" prop="customer_code">
              <el-input v-model="form.customer_code" placeholder="请输入客户编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="客户名称" prop="customer_name">
              <el-input v-model="form.customer_name" placeholder="请输入客户名称" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户类型" prop="customer_type">
              <el-select v-model="form.customer_type" placeholder="请选择客户类型" style="width: 100%">
                <el-option label="企业" :value="1" />
                <el-option label="个人" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="客户等级" prop="customer_level">
              <el-select v-model="form.customer_level" placeholder="请选择客户等级" style="width: 100%">
                <el-option label="重要" :value="1" />
                <el-option label="普通" :value="2" />
                <el-option label="一般" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属行业">
              <el-input v-model="form.industry" placeholder="请输入所属行业" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系人">
              <el-input v-model="form.contact_person" placeholder="请输入联系人" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contact_phone">
              <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系邮箱" prop="contact_email">
              <el-input v-model="form.contact_email" placeholder="请输入联系邮箱" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="详细地址">
          <el-input v-model="form.address" type="textarea" :rows="2" placeholder="请输入详细地址" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="信用额度">
              <el-input-number
                v-model="form.credit_limit"
                :min="0"
                :precision="2"
                :controls="false"
                placeholder="请输入信用额度"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="账期天数">
              <el-input-number
                v-model="form.credit_days"
                :min="0"
                :max="365"
                placeholder="请输入账期天数"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态">
              <el-switch
                v-model="form.status"
                :active-value="1"
                :inactive-value="0"
                active-text="正常"
                inactive-text="停用"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注信息" />
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
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import {
  getCustomerList,
  createCustomer,
  updateCustomer,
  deleteCustomer
} from '@/api/customer'

const formRef = ref(null)
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const tableData = ref([])
const isEdit = ref(false)

const searchForm = reactive({
  customer_code: '',
  customer_name: '',
  customer_type: null,
  customer_level: null,
  status: null
})

const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

const form = reactive({
  id: null,
  customer_code: '',
  customer_name: '',
  customer_type: 1,
  customer_level: 2,
  industry: '',
  contact_person: '',
  contact_phone: '',
  contact_email: '',
  address: '',
  credit_limit: 0,
  credit_days: 0,
  status: 1,
  remark: ''
})

const rules = {
  customer_code: [
    { required: true, message: '请输入客户编码', trigger: 'blur' }
  ],
  customer_name: [
    { required: true, message: '请输入客户名称', trigger: 'blur' }
  ],
  customer_type: [
    { required: true, message: '请选择客户类型', trigger: 'change' }
  ],
  customer_level: [
    { required: true, message: '请选择客户等级', trigger: 'change' }
  ],
  contact_phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  contact_email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 加载客户列表
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...searchForm
    }
    const res = await getCustomerList(params)
    tableData.value = res.data.results
    pagination.total = res.data.count
  } catch (error) {
    ElMessage.error('加载客户数据失败')
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

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    customer_code: '',
    customer_name: '',
    customer_type: null,
    customer_level: null,
    status: null
  })
  pagination.page = 1
  loadData()
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增客户'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑客户'
  Object.assign(form, {
    id: row.id,
    customer_code: row.customer_code,
    customer_name: row.customer_name,
    customer_type: row.customer_type,
    customer_level: row.customer_level,
    industry: row.industry || '',
    contact_person: row.contact_person || '',
    contact_phone: row.contact_phone || '',
    contact_email: row.contact_email || '',
    address: row.address || '',
    credit_limit: row.credit_limit || 0,
    credit_days: row.credit_days || 0,
    status: row.status,
    remark: row.remark || ''
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除客户"${row.customer_name}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteCustomer(row.id)
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
          await updateCustomer(data.id, data)
          ElMessage.success('编辑成功')
        } else {
          await createCustomer(data)
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
    customer_code: '',
    customer_name: '',
    customer_type: 1,
    customer_level: 2,
    industry: '',
    contact_person: '',
    contact_phone: '',
    contact_email: '',
    address: '',
    credit_limit: 0,
    credit_days: 0,
    status: 1,
    remark: ''
  })
}

// 分页
const handleSizeChange = (size) => {
  pagination.page_size = size
  loadData()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.customer-container {
  width: 100%;
  height: 100%;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .search-bar {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
}
</style>
