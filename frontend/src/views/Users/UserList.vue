<template>
  <div class="user-container">
    <el-card shadow="never">
      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="用户名">
          <el-input 
            v-model="searchForm.username" 
            placeholder="请输入用户名" 
            clearable 
            style="width: 180px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="真实姓名">
          <el-input 
            v-model="searchForm.real_name" 
            placeholder="请输入姓名" 
            clearable 
            style="width: 180px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="用户角色">
          <el-select v-model="searchForm.role" placeholder="全部角色" clearable style="width: 160px">
            <el-option label="管理员" value="admin" />
            <el-option label="工作人员" value="staff" />
            <el-option label="推荐单位" value="recommender" />
            <el-option label="申报人" value="applicant" />
            <el-option label="专家" value="expert" />
            <el-option label="评委" value="committee" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            <span>查询</span>
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            <span>重置</span>
          </el-button>
          <el-button type="primary" @click="showCreateDialog" v-if="canCreate">
            <el-icon><Plus /></el-icon>
            <span>新增用户</span>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table 
        :data="users" 
        v-loading="loading" 
        stripe
        border
        style="width: 100%; margin-top: 16px;"
        :header-cell-style="headerCellStyle"
      >
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="username" label="用户名" width="140" show-overflow-tooltip>
          <template #default="{ row }">
            <strong>{{ row.username }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="real_name" label="真实姓名" width="120" align="center" />
        <el-table-column prop="role" label="角色" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)" effect="plain">
              {{ getRoleText(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" width="200" show-overflow-tooltip />
        <el-table-column prop="mobile" label="手机号" width="130" align="center" />
        <el-table-column prop="organization.name" label="所属组织" min-width="200" show-overflow-tooltip />
        <el-table-column prop="is_active" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" effect="plain" size="small">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170" align="center">
          <template #default="{ row }">
            <span style="font-size: 13px;">{{ formatDateTime(row.created_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="380" align="center">
          <template #default="{ row }">
            <div style="display: flex; gap: 8px; justify-content: center;">
              <el-button size="small" type="primary" @click="viewDetail(row.id)">
                <el-icon><View /></el-icon>
                <span>查看</span>
              </el-button>
              <el-button size="small" @click="editUser(row.id)" v-if="canEdit">
                <el-icon><Edit /></el-icon>
                <span>编辑</span>
              </el-button>
              <el-button size="small" @click="resetPassword(row.id)" v-if="canEdit">
                <el-icon><Key /></el-icon>
                <span>重置密码</span>
              </el-button>
              <el-button 
                size="small" 
                :type="row.is_active ? 'warning' : 'success'" 
                @click="toggleStatus(row)" 
                v-if="canEdit"
              >
                <el-icon><Switch /></el-icon>
                <span>{{ row.is_active ? '禁用' : '启用' }}</span>
              </el-button>
              <el-button size="small" type="danger" @click="deleteUser(row.id)" v-if="canDelete">
                <el-icon><Delete /></el-icon>
                <span>删除</span>
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchUsers"
          @current-change="fetchUsers"
          background
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="formData.username" 
            placeholder="请输入用户名" 
            :disabled="!!currentEditId"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!currentEditId">
          <el-input 
            v-model="formData.password" 
            type="password" 
            placeholder="请输入密码" 
            show-password
          />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="formData.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="用户角色" prop="role">
          <el-select v-model="formData.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="管理员" value="admin" />
            <el-option label="工作人员" value="staff" />
            <el-option label="推荐单位管理员" value="recommender" />
            <el-option label="申报人" value="applicant" />
            <el-option label="专家评审" value="expert" />
            <el-option label="评委会成员" value="committee" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属组织" prop="organization_id">
          <el-select v-model="formData.organization_id" placeholder="请选择组织" filterable style="width: 100%">
            <el-option
              v-for="org in organizations"
              :key="org.id"
              :label="org.name"
              :value="org.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="mobile">
          <el-input v-model="formData.mobile" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="formData.is_active" active-text="正常" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitForm" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="passwordDialogVisible"
      title="重置密码"
      width="450px"
    >
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
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
            placeholder="请再次输入密码" 
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleResetPassword" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { View, Edit, Delete, Search, Refresh, Plus, Key, Switch } from '@element-plus/icons-vue'
import { userAPI, organizationAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const users = ref([])
const organizations = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const passwordDialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const passwordFormRef = ref(null)
const currentEditId = ref(null)
const currentResetUserId = ref(null)

const searchForm = ref({
  username: '',
  real_name: '',
  role: ''
})

const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

const formData = ref({
  username: '',
  password: '',
  real_name: '',
  role: '',
  organization_id: null,
  email: '',
  mobile: '',
  is_active: true
})

const passwordForm = ref({
  new_password: '',
  confirm_password: ''
})

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else if (value.length < 6) {
    callback(new Error('密码长度不能少于6位'))
  } else {
    callback()
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.value.new_password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ validator: validatePassword, trigger: 'blur' }],
  real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  email: [{ type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }]
}

const passwordRules = {
  new_password: [{ validator: validatePassword, trigger: 'blur' }],
  confirm_password: [{ validator: validateConfirmPassword, trigger: 'blur' }]
}

const dialogTitle = computed(() => currentEditId.value ? '编辑用户' : '新增用户')
const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }
const canCreate = computed(() => ['admin', 'staff'].includes(authStore.userRole))
const canEdit = computed(() => ['admin', 'staff'].includes(authStore.userRole))
const canDelete = computed(() => authStore.userRole === 'admin')

const getRoleType = (role) => {
  const typeMap = {
    admin: 'danger',
    staff: 'warning',
    recommender: 'primary',
    applicant: 'info',
    expert: 'success',
    committee: 'danger'
  }
  return typeMap[role] || 'info'
}

const getRoleText = (role) => {
  const textMap = {
    admin: '管理员',
    staff: '工作人员',
    recommender: '推荐单位',
    applicant: '申报人',
    expert: '专家',
    committee: '评委'
  }
  return textMap[role] || role
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.value.page - 1) * pagination.value.pageSize,
      limit: pagination.value.pageSize,
      ...searchForm.value
    }
    const response = await userAPI.list(params)
    if (Array.isArray(response)) {
      users.value = response
      pagination.value.total = response.length
    } else {
      users.value = response.items || []
      pagination.value.total = response.total || 0
    }
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const fetchOrganizations = async () => {
  try {
    const response = await organizationAPI.list()
    organizations.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    ElMessage.error('获取组织列表失败')
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  fetchUsers()
}

const handleReset = () => {
  searchForm.value = {
    username: '',
    real_name: '',
    role: ''
  }
  pagination.value.page = 1
  fetchUsers()
}

const showCreateDialog = () => {
  currentEditId.value = null
  resetForm()
  dialogVisible.value = true
}

const editUser = async (id) => {
  try {
    const data = await userAPI.get(id)
    currentEditId.value = id
    formData.value = { 
      ...data,
      password: ''
    }
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取用户详情失败')
  }
}

const handleSubmitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (currentEditId.value) {
          await userAPI.update(currentEditId.value, formData.value)
          ElMessage.success('更新成功')
        } else {
          await userAPI.create(formData.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchUsers()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const resetPassword = (id) => {
  currentResetUserId.value = id
  passwordForm.value = {
    new_password: '',
    confirm_password: ''
  }
  passwordDialogVisible.value = true
}

const handleResetPassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await userAPI.update(currentResetUserId.value, {
          password: passwordForm.value.new_password
        })
        ElMessage.success('密码重置成功')
        passwordDialogVisible.value = false
      } catch (error) {
        ElMessage.error('密码重置失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const toggleStatus = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认${row.is_active ? '禁用' : '启用'}用户 ${row.username}?`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await userAPI.update(row.id, { is_active: !row.is_active })
    ElMessage.success('操作成功')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

const deleteUser = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该用户?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await userAPI.delete(id)
    ElMessage.success('删除成功')
    fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const viewDetail = (id) => {
  router.push({ name: 'UserDetail', params: { id } })
}

const resetForm = () => {
  formData.value = {
    username: '',
    password: '',
    real_name: '',
    role: '',
    organization_id: null,
    email: '',
    mobile: '',
    is_active: true
  }
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

onMounted(() => {
  fetchUsers()
  fetchOrganizations()
})
</script>

<style scoped>
.user-container {
  padding: 0;
}

.search-form {
  margin-bottom: 0;
  padding: 10px 0;
}

.search-form :deep(.el-form-item) {
  margin-bottom: 10px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  padding: 10px 0;
}
</style>
