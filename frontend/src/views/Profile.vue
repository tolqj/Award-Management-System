<template>
  <div class="profile-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span style="font-size: 18px; font-weight: bold;">个人信息</span>
      </template>
    </el-page-header>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <span style="font-weight: bold;">基本信息</span>
          </template>
          
          <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
            <el-form-item label="用户名">
              <el-input v-model="formData.username" disabled />
            </el-form-item>
            <el-form-item label="真实姓名" prop="real_name">
              <el-input v-model="formData.real_name" placeholder="请输入真实姓名" />
            </el-form-item>
            <el-form-item label="用户角色">
              <el-tag :type="getRoleType(formData.role)" effect="plain">
                {{ getRoleText(formData.role) }}
              </el-tag>
            </el-form-item>
            <el-form-item label="所属组织">
              <el-input :model-value="formData.organization?.name" disabled />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="formData.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="手机号" prop="mobile">
              <el-input v-model="formData.mobile" placeholder="请输入手机号" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleUpdate" :loading="submitting">
                <el-icon><Check /></el-icon>
                <span>保存修改</span>
              </el-button>
              <el-button @click="showChangePassword">
                <el-icon><Lock /></el-icon>
                <span>修改密码</span>
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never">
          <template #header>
            <span style="font-weight: bold;">账号状态</span>
          </template>
          
          <div class="status-info">
            <div class="status-item">
              <span class="label">账号状态：</span>
              <el-tag :type="formData.is_active ? 'success' : 'danger'">
                {{ formData.is_active ? '正常' : '禁用' }}
              </el-tag>
            </div>
            <div class="status-item">
              <span class="label">创建时间：</span>
              <span>{{ formatDateTime(formData.created_at) }}</span>
            </div>
            <div class="status-item">
              <span class="label">更新时间：</span>
              <span>{{ formatDateTime(formData.updated_at) }}</span>
            </div>
          </div>
        </el-card>

        <el-card shadow="never" style="margin-top: 20px;">
          <template #header>
            <span style="font-weight: bold;">操作记录</span>
          </template>
          
          <el-empty description="暂无操作记录" :image-size="100" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 修改密码对话框 -->
    <ChangePassword v-model:visible="passwordDialogVisible" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Check, Lock } from '@element-plus/icons-vue'
import { userAPI } from '@/api'
import { useAuthStore } from '@/store/auth'
import ChangePassword from '@/components/ChangePassword.vue'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref(null)
const submitting = ref(false)
const passwordDialogVisible = ref(false)

const formData = ref({
  username: '',
  real_name: '',
  role: '',
  organization: null,
  email: '',
  mobile: '',
  is_active: true,
  created_at: '',
  updated_at: ''
})

const rules = {
  real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  email: [{ type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }]
}

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

const fetchUserInfo = async () => {
  try {
    const data = await userAPI.get(authStore.user.id)
    formData.value = data
  } catch (error) {
    ElMessage.error('获取个人信息失败')
  }
}

const handleUpdate = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await userAPI.update(authStore.user.id, {
          real_name: formData.value.real_name,
          email: formData.value.email,
          mobile: formData.value.mobile
        })
        ElMessage.success('保存成功')
        await authStore.fetchUser()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '保存失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const showChangePassword = () => {
  passwordDialogVisible.value = true
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.status-item {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.status-item .label {
  color: #909399;
  min-width: 80px;
}
</style>
