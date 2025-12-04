<template>
  <div class="detail-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span style="font-size: 18px; font-weight: bold;">奖项详情</span>
      </template>
    </el-page-header>

    <el-card shadow="never" style="margin-top: 20px;" v-loading="loading">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-weight: bold; font-size: 16px;">基本信息</span>
          <el-tag :type="getLevelType(detail.level)" size="large" effect="plain">
            {{ getLevelText(detail.level) }}
          </el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="奖项名称" :span="2">
          <strong style="font-size: 15px;">{{ detail.name }}</strong>
        </el-descriptions-item>
        <el-descriptions-item label="奖项代码">{{ detail.code }}</el-descriptions-item>
        <el-descriptions-item label="年度">{{ detail.year }}</el-descriptions-item>
        <el-descriptions-item label="奖项等级">
          <el-tag :type="getLevelType(detail.level)" effect="plain">
            {{ getLevelText(detail.level) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detail.status === 'active' ? 'success' : 'info'" effect="plain">
            {{ detail.status === 'active' ? '活跃' : '未激活' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申报开始时间">{{ formatDateTime(detail.application_start) }}</el-descriptions-item>
        <el-descriptions-item label="申报结束时间">{{ formatDateTime(detail.application_end) }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
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
              <el-icon :size="32"><List /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">奖项轮次</div>
              <div class="stat-value">{{ statistics.cycles || 0 }}</div>
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
              <el-icon :size="32"><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">已通过</div>
              <div class="stat-value">{{ statistics.approved || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: #f56c6c">
              <el-icon :size="32"><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">评审中</div>
              <div class="stat-value">{{ statistics.reviewing || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 奖项轮次列表 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header>
        <span style="font-weight: bold;">奖项轮次</span>
      </template>
      <el-table :data="cycles" border :header-cell-style="headerCellStyle">
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="cycle_name" label="轮次名称" min-width="200" />
        <el-table-column prop="quota" label="名额限制" width="100" align="center" />
        <el-table-column prop="budget" label="预算(元)" width="140" align="center">
          <template #default="{ row }">
            <el-text type="success">{{ row.budget ? row.budget.toLocaleString() : '-' }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120" align="center">
          <template #default="{ row }">
            {{ formatDate(row.start_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="end_date" label="结束日期" width="120" align="center">
          <template #default="{ row }">
            {{ formatDate(row.end_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'" effect="plain" size="small">
              {{ row.status === 'active' ? '活跃' : '未激活' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 申报项目列表 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header>
        <span style="font-weight: bold;">申报项目</span>
      </template>
      <el-table :data="applications" border :header-cell-style="headerCellStyle">
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="title" label="项目名称" min-width="300" show-overflow-tooltip />
        <el-table-column prop="leader_name" label="负责人" width="110" align="center" />
        <el-table-column prop="applicant_unit.name" label="申报单位" width="200" show-overflow-tooltip />
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
        <el-button type="primary" @click="editAward" v-if="canEdit">
          <el-icon><Edit /></el-icon>
          <span>编辑奖项</span>
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Back, Edit, List, Document, Check, Clock } from '@element-plus/icons-vue'
import { awardAPI, applicationAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const detail = ref({})
const statistics = ref({})
const cycles = ref([])
const applications = ref([])
const loading = ref(false)

const awardId = route.params.id

const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }

const canEdit = computed(() => ['admin', 'staff'].includes(authStore.userRole))

const getLevelType = (level) => {
  const typeMap = {
    special: 'danger',
    first: 'warning',
    second: 'success',
    third: 'info',
    industry: 'primary'
  }
  return typeMap[level] || 'info'
}

const getLevelText = (level) => {
  const textMap = {
    special: '特等奖',
    first: '一等奖',
    second: '二等奖',
    third: '三等奖',
    industry: '行业奖'
  }
  return textMap[level] || level
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

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return dateStr.split('T')[0]
}

const fetchDetail = async () => {
  loading.value = true
  try {
    detail.value = await awardAPI.get(awardId)
    await Promise.all([
      fetchCycles(),
      fetchApplications(),
      fetchStatistics()
    ])
  } catch (error) {
    ElMessage.error('获取奖项详情失败')
  } finally {
    loading.value = false
  }
}

const fetchCycles = async () => {
  try {
    const response = await awardAPI.listCycles({ award_id: awardId })
    cycles.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取奖项轮次失败', error)
  }
}

const fetchApplications = async () => {
  try {
    const response = await applicationAPI.list({ award_id: awardId, limit: 20 })
    applications.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取申报列表失败', error)
  }
}

const fetchStatistics = async () => {
  try {
    const [cyclesResp, appsResp] = await Promise.all([
      awardAPI.listCycles({ award_id: awardId }),
      applicationAPI.list({ award_id: awardId })
    ])
    
    const cycleList = Array.isArray(cyclesResp) ? cyclesResp : (cyclesResp.items || [])
    const appList = Array.isArray(appsResp) ? appsResp : (appsResp.items || [])
    
    statistics.value = {
      cycles: cycleList.length,
      applications: appList.length,
      approved: appList.filter(app => app.submission_status === 'approved').length,
      reviewing: appList.filter(app => ['reviewing', 'expert_review'].includes(app.submission_status)).length
    }
  } catch (error) {
    console.error('获取统计信息失败', error)
  }
}

const goBack = () => {
  router.back()
}

const editAward = () => {
  router.push({ name: 'Awards', query: { edit: awardId } })
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
