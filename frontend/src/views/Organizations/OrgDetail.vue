<template>
  <div class="detail-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span style="font-size: 18px; font-weight: bold;">组织详情</span>
      </template>
    </el-page-header>

    <el-card shadow="never" style="margin-top: 20px;" v-loading="loading">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-weight: bold; font-size: 16px;">基本信息</span>
          <el-tag :type="getTypeColor(detail.org_type)" size="large" effect="plain">
            {{ getTypeText(detail.org_type) }}
          </el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="组织名称" :span="2">
          <strong style="font-size: 15px;">{{ detail.name }}</strong>
        </el-descriptions-item>
        <el-descriptions-item label="组织代码">{{ detail.code }}</el-descriptions-item>
        <el-descriptions-item label="组织类型">
          <el-tag :type="getTypeColor(detail.org_type)" effect="plain">
            {{ getTypeText(detail.org_type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="联系人">{{ detail.contact_person }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ detail.contact_phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱" :span="2">{{ detail.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="地址" :span="2">{{ detail.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="组织描述" :span="2">
          <div style="white-space: pre-line;">{{ detail.description || '-' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDateTime(detail.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDateTime(detail.updated_at) }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 统计信息 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: #409eff">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">用户数量</div>
              <div class="stat-value">{{ statistics.users || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: #67c23a">
              <el-icon :size="32"><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">申报项目</div>
              <div class="stat-value">{{ statistics.applications || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: #e6a23c">
              <el-icon :size="32"><Medal /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">获奖项目</div>
              <div class="stat-value">{{ statistics.awards || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: #f56c6c">
              <el-icon :size="32"><Star /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">专家数量</div>
              <div class="stat-value">{{ statistics.experts || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 用户列表 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header>
        <span style="font-weight: bold;">组织用户</span>
      </template>
      <el-table :data="users" border :header-cell-style="headerCellStyle">
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="real_name" label="真实姓名" width="120" align="center" />
        <el-table-column prop="role" label="角色" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)" effect="plain" size="small">
              {{ getRoleText(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="200" show-overflow-tooltip />
        <el-table-column prop="mobile" label="手机号" width="130" align="center" />
        <el-table-column prop="is_active" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" effect="plain" size="small">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 申报项目 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header>
        <span style="font-weight: bold;">申报项目</span>
      </template>
      <el-table :data="applications" border :header-cell-style="headerCellStyle">
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="title" label="项目名称" min-width="300" show-overflow-tooltip />
        <el-table-column prop="leader_name" label="负责人" width="110" align="center" />
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

    <!-- 操作按钮 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <el-space>
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>
          <span>返回列表</span>
        </el-button>
        <el-button type="primary" @click="editOrganization" v-if="canEdit">
          <el-icon><Edit /></el-icon>
          <span>编辑组织</span>
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Back, Edit, User, Document, Medal, Star } from '@element-plus/icons-vue'
import { organizationAPI, userAPI, applicationAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const detail = ref({})
const statistics = ref({})
const users = ref([])
const applications = ref([])
const loading = ref(false)

const orgId = route.params.id

const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }

const canEdit = computed(() => ['admin', 'staff'].includes(authStore.userRole))

const getTypeColor = (type) => {
  const colorMap = {
    enterprise: 'primary',
    university: 'success',
    research_institute: 'warning',
    recommender: 'danger',
    institute: 'warning',
    association: 'info',
    other: 'info'
  }
  return colorMap[type] || 'info'
}

const getTypeText = (type) => {
  const textMap = {
    enterprise: '企业',
    university: '高校',
    research_institute: '科研院所',
    recommender: '推荐单位',
    institute: '研究院所',
    association: '行业协会',
    other: '其他'
  }
  return textMap[type] || type
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
    detail.value = await organizationAPI.get(orgId)
    await Promise.all([
      fetchUsers(),
      fetchApplications(),
      fetchStatistics()
    ])
  } catch (error) {
    ElMessage.error('获取组织详情失败')
  } finally {
    loading.value = false
  }
}

const fetchUsers = async () => {
  try {
    const response = await userAPI.list({ organization_id: orgId, limit: 100 })
    users.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取用户列表失败', error)
  }
}

const fetchApplications = async () => {
  try {
    const response = await applicationAPI.list({ applicant_unit_id: orgId, limit: 20 })
    applications.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取申报列表失败', error)
  }
}

const fetchStatistics = async () => {
  try {
    const [usersResp, appsResp] = await Promise.all([
      userAPI.list({ organization_id: orgId }),
      applicationAPI.list({ applicant_unit_id: orgId })
    ])
    
    const userList = Array.isArray(usersResp) ? usersResp : (usersResp.items || [])
    const appList = Array.isArray(appsResp) ? appsResp : (appsResp.items || [])
    
    statistics.value = {
      users: userList.length,
      applications: appList.length,
      awards: appList.filter(app => app.submission_status === 'approved').length,
      experts: userList.filter(u => u.role === 'expert').length
    }
  } catch (error) {
    console.error('获取统计信息失败', error)
  }
}

const goBack = () => {
  router.back()
}

const editOrganization = () => {
  router.push({ name: 'Organizations', query: { edit: orgId } })
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
