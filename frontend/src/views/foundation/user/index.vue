<template>
  <div class="user-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增用户
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="用户名">
            <el-input
              v-model="searchForm.username"
              placeholder="请输入用户名"
              clearable
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="员工编号">
            <el-input
              v-model="searchForm.employee_no"
              placeholder="请输入员工编号"
              clearable
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="部门">
            <el-tree-select
              v-model="searchForm.department"
              :data="departmentTree"
              :props="{ label: 'name', value: 'id' }"
              clearable
              placeholder="请选择部门"
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

      <!-- 用户列表 -->
      <el-table
        :data="tableData"
        border
        stripe
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="employee_no" label="员工编号" width="120" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="department_name" label="部门" width="150" />
        <el-table-column prop="position" label="岗位" width="120" />
        <el-table-column prop="gender" label="性别" width="60" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.gender === 'M'" type="primary" size="small">男</el-tag>
            <el-tag v-else-if="row.gender === 'F'" type="danger" size="small">女</el-tag>
            <el-tag v-else type="info" size="small">未知</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.status === 'active'" type="success" size="small">在职</el-tag>
            <el-tag v-else-if="row.status === 'leave'" type="danger" size="small">离职</el-tag>
            <el-tag v-else type="warning" size="small">试用</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="账号状态" width="90" align="center">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_active"
              @change="handleStatusChange(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="last_login" label="最后登录" width="160" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="warning" size="small" link @click="handleResetPassword(row)">
              重置密码
            </el-button>
            <el-button type="success" size="small" link @click="handleAssignRole(row)">
              分配角色
            </el-button>
            <el-button type="danger" size="small" link @click="handleDelete(row)">
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
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="员工编号" prop="employee_no">
              <el-input v-model="form.employee_no" placeholder="请输入员工编号" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20" v-if="!isEdit">
          <el-col :span="12">
            <el-form-item label="密码" prop="password">
              <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="确认密码" prop="password_confirm">
              <el-input v-model="form.password_confirm" type="password" placeholder="请确认密码" show-password />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部门" prop="department">
              <el-tree-select
                v-model="form.department"
                :data="departmentTree"
                :props="{ label: 'name', value: 'id' }"
                clearable
                placeholder="请选择部门"
                check-strictly
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="岗位">
              <el-input v-model="form.position" placeholder="请输入岗位" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别">
              <el-radio-group v-model="form.gender">
                <el-radio label="M">男</el-radio>
                <el-radio label="F">女</el-radio>
                <el-radio label="U">未知</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-select v-model="form.status" placeholder="请选择状态">
                <el-option label="在职" value="active" />
                <el-option label="试用" value="probation" />
                <el-option label="离职" value="leave" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="生日">
              <el-date-picker
                v-model="form.birthday"
                type="date"
                placeholder="请选择生日"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="入职日期">
              <el-date-picker
                v-model="form.entry_date"
                type="date"
                placeholder="请选择入职日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
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

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="passwordDialogVisible"
      title="重置密码"
      width="400px"
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
      >
        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="passwordForm.new_password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input
            v-model="passwordForm.confirm_password"
            type="password"
            placeholder="请确认新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handlePasswordSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 分配角色对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      title="分配角色"
      width="500px"
    >
      <el-form label-width="80px">
        <el-form-item label="角色">
          <el-checkbox-group v-model="selectedRoles">
            <el-checkbox
              v-for="role in roleList"
              :key="role.id"
              :label="role.id"
            >
              {{ role.name }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRoleSubmit" :loading="submitting">
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
  getUserList,
  createUser,
  updateUser,
  deleteUser,
  resetUserPassword
} from '@/api/user'
import { getDepartmentTree } from '@/api/department'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const passwordDialogVisible = ref(false)
const roleDialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const tableData = ref([])
const departmentTree = ref([])
const roleList = ref([])
const selectedRoles = ref([])
const currentUserId = ref(null)
const formRef = ref(null)
const passwordFormRef = ref(null)

// 搜索表单
const searchForm = reactive({
  username: '',
  employee_no: '',
  department: null,
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
  username: '',
  employee_no: '',
  password: '',
  password_confirm: '',
  email: '',
  phone: '',
  department: null,
  position: '',
  gender: 'U',
  birthday: '',
  entry_date: '',
  status: 'active',
  remark: '',
  is_active: true
})

// 密码表单
const passwordForm = reactive({
  new_password: '',
  confirm_password: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' }
  ],
  employee_no: [
    { required: true, message: '请输入员工编号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  password_confirm: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  department: [
    { required: true, message: '请选择部门', trigger: 'change' }
  ]
}

// 密码验证规则
const passwordRules = {
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 加载部门树
const loadDepartmentTree = async () => {
  try {
    const res = await getDepartmentTree()
    departmentTree.value = res.data
  } catch (error) {
    console.error('加载部门树失败:', error)
  }
}

// 加载用户列表
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }
    const res = await getUserList(params)
    if (res.data && res.data.results) {
      tableData.value = res.data.results
      pagination.total = res.data.count
    } else {
      tableData.value = res.data || []
    }
  } catch (error) {
    ElMessage.error('加载用户列表失败')
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
    username: '',
    employee_no: '',
    department: null,
    is_active: null
  })
  handleSearch()
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增用户'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑用户'
  Object.assign(form, {
    id: row.id,
    username: row.username,
    employee_no: row.employee_no,
    email: row.email,
    phone: row.phone,
    department: row.department,
    position: row.position,
    gender: row.gender || 'U',
    birthday: row.birthday,
    entry_date: row.entry_date,
    status: row.status,
    remark: row.remark,
    is_active: row.is_active
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除用户"${row.username}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteUser(row.id)
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
    await updateUser(row.id, { is_active: row.is_active })
    ElMessage.success('状态修改成功')
  } catch (error) {
    row.is_active = !row.is_active
    ElMessage.error('状态修改失败')
    console.error(error)
  }
}

// 重置密码
const handleResetPassword = (row) => {
  currentUserId.value = row.id
  passwordForm.new_password = ''
  passwordForm.confirm_password = ''
  passwordDialogVisible.value = true
}

// 分配角色
const handleAssignRole = (row) => {
  currentUserId.value = row.id
  selectedRoles.value = row.roles || []
  roleDialogVisible.value = true
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
          delete data.password
          delete data.password_confirm
          await updateUser(data.id, data)
          ElMessage.success('编辑成功')
        } else {
          await createUser(data)
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

// 提交密码重置
const handlePasswordSubmit = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await resetUserPassword(currentUserId.value, {
          new_password: passwordForm.new_password
        })
        ElMessage.success('密码重置成功')
        passwordDialogVisible.value = false
      } catch (error) {
        const errorMsg = error.response?.data?.message || '密码重置失败'
        ElMessage.error(errorMsg)
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

// 提交角色分配
const handleRoleSubmit = async () => {
  submitting.value = true
  try {
    await updateUser(currentUserId.value, { roles: selectedRoles.value })
    ElMessage.success('角色分配成功')
    roleDialogVisible.value = false
    loadData()
  } catch (error) {
    const errorMsg = error.response?.data?.message || '角色分配失败'
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
    username: '',
    employee_no: '',
    password: '',
    password_confirm: '',
    email: '',
    phone: '',
    department: null,
    position: '',
    gender: 'U',
    birthday: '',
    entry_date: '',
    status: 'active',
    remark: '',
    is_active: true
  })
}

onMounted(() => {
  loadDepartmentTree()
  loadData()
})
</script>

<style scoped lang="scss">
.user-container {
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
