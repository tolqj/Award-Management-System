<template>
  <div class="detail-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span style="font-size: 18px; font-weight: bold;">用户详情</span>
      </template>
    </el-page-header>

    <el-card shadow="never" style="margin-top: 20px;" v-loading="loading">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-weight: bold; font-size: 16px;">基本信息</span>
          <el-tag :type="detail.is_active ? 'success' : 'danger'" size="large">
            {{ detail.is_active ? '正常' : '禁用' }}
          </el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户名">
          <strong style="font-size: 15px;">{{ detail.username }}</strong>
        </el-descriptions-item>
        <el-descriptions-item label="真实姓名">{{ detail.real_name }}</el-descriptions-item>
        <el-descriptions-item label="用户角色">
          <el-tag :type="getRoleType(detail.role)" effect="plain">
            {{ getRoleText(detail.role) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="所属组织">{{ detail.organization?.name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ detail.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ detail.mobile || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDateTime(detail.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDateTime(detail.updated_at) }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 关联数据统计 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: #409eff">
              <el-icon :size="32"><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">申报项目</div>
              <div class="stat-value">{{ statistics.applications || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: #67c23a">
              <el-icon :size="32"><Edit /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">评审任务</div>
              <div class="stat-value">{{ statistics.reviews || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: #e6a23c">
              <el-icon :size="32"><List /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">决议记录</div>
              <div class="stat-value">{{ statistics.decisions || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近活动 -->
    <el-card shadow="never" style="margin-top: 20px;" v-if="detail.role === 'applicant'">
      <template #header>
        <span style="font-weight: bold;">最近申报项目</span>
      </template>
      <el-table :data="recentApplications" border :header-cell-style="headerCellStyle">
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="title" label="项目名称" min-width="300" show-overflow-tooltip />
        <el-table-column prop="submission_status" label="状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.submission_status)" effect="plain" size="small">
              {{ getStatusText(row.submission_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="submission_time" label="提交时间" width="170" align="center">
          <template #default="{ row }">
            {{ formatDateTime(row.submission_time) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="never" style="margin-top: 20px;" v-if="detail.role === 'expert'">
      <template #header>
        <span style="font-weight: bold;">最近评审任务</span>
      </template>
      <el-table :data="recentReviews" border :header-cell-style="headerCellStyle">
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="application.title" label="项目名称" min-width="300" show-overflow-tooltip />
        <el-table-column prop="total_score" label="评分" width="100" align="center">
          <template #default="{ row }">
            <el-text type="primary" style="font-weight: bold; font-size: 16px;">{{ row.total_score }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'submitted' ? 'success' : 'warning'" effect="plain" size="small">
              {{ row.status === 'submitted' ? '已提交' : '待完成' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="submitted_at" label="提交时间" width="170" align="center">
          <template #default="{ row }">
            {{ formatDateTime(row.submitted_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 操作按钮 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <el-space>
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>
          <span>返回列表</span>
        </el-button>
        <el-button type="primary" @click="editUser" v-if="canEdit">
          <el-icon><Edit /></el-icon>
          <span>编辑用户</span>
        </el-button>
        <el-button @click="resetPassword" v-if="canEdit">
          <el-icon><Key /></el-icon>
          <span>重置密码</span>
        </el-button>
        <el-button :type="detail.is_active ? 'warning' : 'success'" @click="toggleStatus" v-if="canEdit">
          <el-icon><Switch /></el-icon>
          <span>{{ detail.is_active ? '禁用账号' : '启用账号' }}</span>
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Back, Edit, Key, Switch, Document, List } from '@element-plus/icons-vue'
import { userAPI, applicationAPI, reviewAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const detail = ref({})
const statistics = ref({})
const recentApplications = ref([])
const recentReviews = ref([])
const loading = ref(false)

const userId = route.params.id

const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }

const canEdit = computed(() => ['admin', 'staff'].includes(authStore.userRole))

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

const getStatusType = (status) => {
  const statusMap = {
    draft: 'info',
    submitted: 'warning',
    reviewing: 'primary',
    expert_review: 'primary',
    approved: 'success',
    rejected: 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    draft: '草稿',
    submitted: '已提交',
    reviewing: '初审中',
    expert_review: '专家评审中',
    approved: '已通过',
    rejected: '未通过'
  }
  return statusMap[status] || status
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

const fetchDetail = async () => {
  loading.value = true
  try {
    detail.value = await userAPI.get(userId)
    await fetchStatistics()
    if (detail.value.role === 'applicant') {
      await fetchRecentApplications()
    } else if (detail.value.role === 'expert') {
      await fetchRecentReviews()
    }
  } catch (error) {
    ElMessage.error('获取用户详情失败')
  } finally {
    loading.value = false
  }
}

const fetchStatistics = async () => {
  try {
    const [apps, reviews] = await Promise.all([
      applicationAPI.list({ applicant_user_id: userId }).catch(() => []),
      reviewAPI.myReviews({ expert_id: userId }).catch(() => [])
    ])
    statistics.value = {
      applications: Array.isArray(apps) ? apps.length : (apps.total || 0),
      reviews: Array.isArray(reviews) ? reviews.length : (reviews.total || 0),
      decisions: 0
    }
  } catch (error) {
    console.error('获取统计信息失败', error)
  }
}

const fetchRecentApplications = async () => {
  try {
    const response = await applicationAPI.list({ applicant_user_id: userId, limit: 5 })
    recentApplications.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取申报列表失败', error)
  }
}

const fetchRecentReviews = async () => {
  try {
    const response = await reviewAPI.myReviews({ limit: 5 })
    recentReviews.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取评审列表失败', error)
  }
}

const goBack = () => {
  router.back()
}

const editUser = () => {
  router.push({ name: 'Users', query: { edit: userId } })
}

const resetPassword = () => {
  ElMessage.info('请返回用户列表页面进行密码重置')
}

const toggleStatus = async () => {
  try {
    await ElMessageBox.confirm(
      `确认${detail.value.is_active ? '禁用' : '启用'}用户 ${detail.value.username}?`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await userAPI.update(userId, { is_active: !detail.value.is_active })
    ElMessage.success('操作成功')
    fetchDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  fetchDetail()
})
</script>

<style scoped>
.detail-container {
  padding: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}
</style>
