<template>
  <div class="detail-container">
    <el-page-header @back="goBack" title="返回">
      <template #content>
        <span style="font-size: 18px; font-weight: bold;">申报详情</span>
      </template>
    </el-page-header>

    <el-card shadow="never" style="margin-top: 20px;" v-loading="loading">
      <!-- 基本信息 -->
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-weight: bold; font-size: 16px;">基本信息</span>
          <div>
            <el-tag :type="getStatusType(detail.submission_status)" effect="plain" size="large">
              {{ getStatusText(detail.submission_status) }}
            </el-tag>
          </div>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="项目名称" :span="2">
          <strong style="font-size: 15px;">{{ detail.title }}</strong>
        </el-descriptions-item>
        <el-descriptions-item label="项目类别">{{ detail.category }}</el-descriptions-item>
        <el-descriptions-item label="当前阶段">{{ detail.current_stage || '-' }}</el-descriptions-item>
        <el-descriptions-item label="负责人">{{ detail.leader_name }}</el-descriptions-item>
        <el-descriptions-item label="负责人职称">{{ detail.leader_title }}</el-descriptions-item>
        <el-descriptions-item label="申报单位" :span="2">{{ detail.applicant_unit?.name }}</el-descriptions-item>
        <el-descriptions-item label="申报人">{{ detail.applicant_user?.real_name }}</el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ formatDateTime(detail.submission_time) }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 团队成员 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header>
        <span style="font-weight: bold;">团队成员</span>
      </template>
      <div style="padding: 10px 0;">
        <el-tag v-for="(member, index) in teamMembersList" :key="index" style="margin-right: 10px; margin-bottom: 10px;">
          {{ member }}
        </el-tag>
        <span v-if="!detail.team_members" style="color: #909399;">暂无</span>
      </div>
    </el-card>

    <!-- 项目详情 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header>
        <span style="font-weight: bold;">项目详情</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="24">
          <div class="detail-section">
            <div class="section-title">项目摘要</div>
            <div class="section-content">{{ detail.summary || '-' }}</div>
          </div>
        </el-col>

        <el-col :span="24">
          <div class="detail-section">
            <div class="section-title">技术详情</div>
            <div class="section-content">{{ detail.technical_details || '-' }}</div>
          </div>
        </el-col>

        <el-col :span="24">
          <div class="detail-section">
            <div class="section-title">创新点</div>
            <div class="section-content" style="white-space: pre-line;">{{ detail.innovation_points || '-' }}</div>
          </div>
        </el-col>

        <el-col :span="24">
          <div class="detail-section">
            <div class="section-title">应用价值</div>
            <div class="section-content">{{ detail.application_value || '-' }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 效益分析 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header>
        <span style="font-weight: bold;">效益分析</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="detail-section">
            <div class="section-title">经济效益</div>
            <div class="section-content">{{ detail.economic_benefit || '-' }}</div>
          </div>
        </el-col>

        <el-col :span="12">
          <div class="detail-section">
            <div class="section-title">社会效益</div>
            <div class="section-content">{{ detail.social_benefit || '-' }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 评审信息 -->
    <el-card shadow="never" style="margin-top: 20px;" v-if="reviews.length > 0">
      <template #header>
        <span style="font-weight: bold;">评审信息</span>
      </template>

      <el-table :data="reviews" border :header-cell-style="headerCellStyle">
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column label="评审专家" align="center" width="120">
          <template #default="{ row }">
            {{ row.is_anonymous ? '匿名专家' : row.expert?.real_name }}
          </template>
        </el-table-column>
        <el-table-column prop="total_score" label="总分" width="100" align="center">
          <template #default="{ row }">
            <el-text type="primary" size="large" style="font-weight: bold;">{{ row.total_score }}</el-text>
          </template>
        </el-table-column>
        <el-table-column label="评分详情" min-width="300">
          <template #default="{ row }">
            <el-space wrap>
              <el-tag v-for="(value, key) in row.scores_json" :key="key" type="info">
                {{ key }}: {{ value }}分
              </el-tag>
            </el-space>
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="评审意见" min-width="250" show-overflow-tooltip />
        <el-table-column prop="submitted_at" label="提交时间" width="170" align="center">
          <template #default="{ row }">
            {{ formatDateTime(row.submitted_at) }}
          </template>
        </el-table-column>
      </el-table>

      <div v-if="detail.score_summary_json" style="margin-top: 20px; padding: 15px; background: #f5f7fa; border-radius: 4px;">
        <el-row :gutter="20">
          <el-col :span="6">
            <div style="text-align: center;">
              <div style="font-size: 24px; font-weight: bold; color: #409eff;">{{ detail.score_summary_json.average_score }}</div>
              <div style="color: #909399; margin-top: 5px;">平均分</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div style="text-align: center;">
              <div style="font-size: 24px; font-weight: bold; color: #67c23a;">{{ detail.score_summary_json.max_score }}</div>
              <div style="color: #909399; margin-top: 5px;">最高分</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div style="text-align: center;">
              <div style="font-size: 24px; font-weight: bold; color: #e6a23c;">{{ detail.score_summary_json.min_score }}</div>
              <div style="color: #909399; margin-top: 5px;">最低分</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div style="text-align: center;">
              <div style="font-size: 24px; font-weight: bold; color: #909399;">{{ detail.score_summary_json.review_count }}</div>
              <div style="color: #909399; margin-top: 5px;">评审数</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 决议信息 -->
    <el-card shadow="never" style="margin-top: 20px;" v-if="decisions.length > 0">
      <template #header>
        <span style="font-weight: bold;">评审委员会决议</span>
      </template>

      <el-timeline>
        <el-timeline-item
          v-for="decision in decisions"
          :key="decision.id"
          :timestamp="formatDateTime(decision.meeting_date)"
          placement="top"
        >
          <el-card>
            <div style="margin-bottom: 10px;">
              <el-tag :type="decision.decision === 'approved' ? 'success' : 'danger'">
                {{ decision.decision === 'approved' ? '通过' : '未通过' }}
              </el-tag>
              <span v-if="decision.award_grade" style="margin-left: 10px;">
                建议奖项等级：<el-tag type="warning">{{ decision.award_grade }}</el-tag>
              </span>
            </div>
            <div style="margin-bottom: 10px;">
              投票结果：
              <el-tag type="success" effect="plain">赞成 {{ decision.vote_for }}</el-tag>
              <el-tag type="danger" effect="plain" style="margin-left: 8px;">反对 {{ decision.vote_against }}</el-tag>
              <el-tag type="info" effect="plain" style="margin-left: 8px;">弃权 {{ decision.vote_abstain }}</el-tag>
            </div>
            <div style="color: #606266;">{{ decision.decision_note }}</div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <!-- 操作按钮 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <el-space>
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>
          <span>返回列表</span>
        </el-button>
        <el-button type="primary" @click="editApplication" v-if="canEdit">
          <el-icon><Edit /></el-icon>
          <span>编辑</span>
        </el-button>
        <el-button type="success" @click="submitApplication" v-if="canSubmit">
          <el-icon><Check /></el-icon>
          <span>提交申报</span>
        </el-button>
        <el-button type="primary" @click="exportPdf">
          <el-icon><Download /></el-icon>
          <span>导出PDF</span>
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Back, Edit, Check, Download } from '@element-plus/icons-vue'
import { applicationAPI, reviewAPI, committeeAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const detail = ref({})
const reviews = ref([])
const decisions = ref([])
const loading = ref(false)

const appId = route.params.id

const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }

const teamMembersList = computed(() => {
  if (!detail.value.team_members) return []
  return detail.value.team_members.split(/[,，、]/).map(m => m.trim()).filter(m => m)
})

const canEdit = computed(() => {
  return detail.value.submission_status === 'draft' && 
         ['admin', 'staff', 'applicant'].includes(authStore.userRole)
})

const canSubmit = computed(() => {
  return detail.value.submission_status === 'draft' && 
         ['admin', 'staff', 'applicant'].includes(authStore.userRole)
})

const getStatusType = (status) => {
  const statusMap = {
    draft: 'info',
    submitted: 'warning',
    reviewing: 'primary',
    expert_review: 'primary',
    final_review: 'primary',
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
    final_review: '终审中',
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
    detail.value = await applicationAPI.get(appId)
  } catch (error) {
    ElMessage.error('获取申报详情失败')
  } finally {
    loading.value = false
  }
}

const fetchReviews = async () => {
  try {
    const response = await reviewAPI.getByApplication(appId)
    reviews.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取评审信息失败', error)
  }
}

const fetchDecisions = async () => {
  try {
    const response = await committeeAPI.getApplicationDecisions(appId)
    decisions.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取决议信息失败', error)
  }
}

const goBack = () => {
  router.back()
}

const editApplication = () => {
  router.push(`/applications/${appId}/edit`)
}

const submitApplication = async () => {
  try {
    await ElMessageBox.confirm('提交后将无法修改，确认提交？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await applicationAPI.submit(appId)
    ElMessage.success('提交成功')
    fetchDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('提交失败')
    }
  }
}

const exportPdf = () => {
  ElMessage.info('导出PDF功能开发中')
}

onMounted(() => {
  fetchDetail()
  fetchReviews()
  fetchDecisions()
})
</script>

<style scoped>
.detail-container {
  padding: 20px;
}

.detail-section {
  margin-bottom: 20px;
}

.section-title {
  font-weight: bold;
  font-size: 14px;
  color: #303133;
  margin-bottom: 10px;
  padding-left: 10px;
  border-left: 3px solid #409eff;
}

.section-content {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
  color: #606266;
  line-height: 1.8;
  min-height: 60px;
}
</style>
