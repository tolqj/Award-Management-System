<template>
  <div class="app-container">
    <el-card shadow="never">
      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="项目名称">
          <el-input 
            v-model="searchForm.title" 
            placeholder="请输入项目名称" 
            clearable 
            style="width: 220px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="申报单位">
          <el-select v-model="searchForm.applicant_unit_id" placeholder="全部单位" clearable style="width: 200px">
            <el-option
              v-for="org in organizations"
              :key="org.id"
              :label="org.name"
              :value="org.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="全部状态" clearable style="width: 160px">
            <el-option label="草稿" value="draft" />
            <el-option label="已提交" value="submitted" />
            <el-option label="初审中" value="reviewing" />
            <el-option label="专家评审中" value="expert_review" />
            <el-option label="终审中" value="final_review" />
            <el-option label="已通过" value="approved" />
            <el-option label="未通过" value="rejected" />
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
            <span>新增申报</span>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table 
        :data="applications" 
        v-loading="loading" 
        stripe
        border
        style="width: 100%; margin-top: 16px;"
        :header-cell-style="headerCellStyle"
      >
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="title" label="项目名称" min-width="300" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="viewDetail(row.id)" :underline="false">
              <strong>{{ row.title }}</strong>
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="leader_name" label="负责人" width="110" align="center" />
        <el-table-column prop="applicant_unit.name" label="申报单位" width="220" show-overflow-tooltip />
        <el-table-column prop="submission_status" label="状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.submission_status)" effect="plain">
              {{ getStatusText(row.submission_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="current_stage" label="当前阶段" width="140" align="center">
          <template #default="{ row }">
            <span style="color: #909399; font-size: 13px;">{{ row.current_stage || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="submission_time" label="提交时间" width="170" align="center">
          <template #default="{ row }">
            <span style="font-size: 13px;">{{ row.submission_time ? formatDate(row.submission_time) : '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="340" align="center">
          <template #default="{ row }">
            <div style="display: flex; gap: 8px; justify-content: center;">
              <el-button size="small" type="primary" @click="viewDetail(row.id)">
                <el-icon><View /></el-icon>
                <span>查看</span>
              </el-button>
              <el-button size="small" @click="editApplication(row.id)" v-if="canEdit(row)">
                <el-icon><Edit /></el-icon>
                <span>编辑</span>
              </el-button>
              <el-button size="small" type="success" @click="submitApplication(row.id)" v-if="canSubmit(row)">
                <el-icon><Check /></el-icon>
                <span>提交</span>
              </el-button>
              <el-button size="small" type="danger" @click="deleteApplication(row.id)" v-if="canDelete(row)">
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
          @size-change="fetchApplications"
          @current-change="fetchApplications"
          background
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      @close="resetForm"
    >
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="奖项轮次" prop="award_cycle_id">
          <el-select v-model="formData.award_cycle_id" placeholder="请选择奖项轮次" style="width: 100%">
            <el-option
              v-for="cycle in awardCycles"
              :key="cycle.id"
              :label="cycle.cycle_name"
              :value="cycle.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称" prop="title">
          <el-input v-model="formData.title" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目类别" prop="category">
          <el-input v-model="formData.category" placeholder="请输入项目类别" />
        </el-form-item>
        <el-form-item label="负责人" prop="leader_name">
          <el-input v-model="formData.leader_name" placeholder="请输入负责人姓名" />
        </el-form-item>
        <el-form-item label="负责人职称" prop="leader_title">
          <el-input v-model="formData.leader_title" placeholder="请输入负责人职称" />
        </el-form-item>
        <el-form-item label="团队成员" prop="team_members">
          <el-input v-model="formData.team_members" type="textarea" :rows="3" placeholder="请输入团队成员，多个成员用逗号分隔" />
        </el-form-item>
        <el-form-item label="项目摘要" prop="summary">
          <el-input v-model="formData.summary" type="textarea" :rows="4" placeholder="请输入项目摘要" />
        </el-form-item>
        <el-form-item label="技术详情" prop="technical_details">
          <el-input v-model="formData.technical_details" type="textarea" :rows="4" placeholder="请输入技术详情" />
        </el-form-item>
        <el-form-item label="创新点" prop="innovation_points">
          <el-input v-model="formData.innovation_points" type="textarea" :rows="3" placeholder="请输入创新点" />
        </el-form-item>
        <el-form-item label="应用价值" prop="application_value">
          <el-input v-model="formData.application_value" type="textarea" :rows="3" placeholder="请输入应用价值" />
        </el-form-item>
        <el-form-item label="经济效益" prop="economic_benefit">
          <el-input v-model="formData.economic_benefit" type="textarea" :rows="3" placeholder="请输入经济效益" />
        </el-form-item>
        <el-form-item label="社会效益" prop="social_benefit">
          <el-input v-model="formData.social_benefit" type="textarea" :rows="3" placeholder="请输入社会效益" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitForm" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { View, Edit, Check, Delete, Search, Refresh, Plus } from '@element-plus/icons-vue'
import { applicationAPI, awardAPI, organizationAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const applications = ref([])
const awardCycles = ref([])
const organizations = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentEditId = ref(null)

const searchForm = ref({
  title: '',
  applicant_unit_id: null,
  status: ''
})

const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

const formData = ref({
  award_cycle_id: null,
  title: '',
  category: '',
  leader_name: '',
  leader_title: '',
  team_members: '',
  summary: '',
  technical_details: '',
  innovation_points: '',
  application_value: '',
  economic_benefit: '',
  social_benefit: ''
})

const rules = {
  award_cycle_id: [{ required: true, message: '请选择奖项轮次', trigger: 'change' }],
  title: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  leader_name: [{ required: true, message: '请输入负责人姓名', trigger: 'blur' }]
}

const dialogTitle = computed(() => currentEditId.value ? '编辑申报' : '新增申报')

const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }

const canCreate = computed(() => ['admin', 'staff', 'applicant'].includes(authStore.userRole))

const canEdit = (row) => {
  if (!row || !row.submission_status) return false
  return row.submission_status === 'draft' && ['admin', 'staff', 'applicant'].includes(authStore.userRole)
}

const canSubmit = (row) => {
  if (!row || !row.submission_status) return false
  return row.submission_status === 'draft' && ['admin', 'staff', 'applicant'].includes(authStore.userRole)
}

const canDelete = (row) => {
  if (!row || !row.submission_status) return false
  return row.submission_status === 'draft' && ['admin', 'staff'].includes(authStore.userRole)
}

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

const formatDate = (dateStr) => {
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

const fetchApplications = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.value.page - 1) * pagination.value.pageSize,
      limit: pagination.value.pageSize,
      ...searchForm.value
    }
    const response = await applicationAPI.list(params)
    if (Array.isArray(response)) {
      applications.value = response
      pagination.value.total = response.length
    } else {
      applications.value = response.items || []
      pagination.value.total = response.total || 0
    }
  } catch (error) {
    ElMessage.error('获取申报列表失败')
  } finally {
    loading.value = false
  }
}

const fetchAwardCycles = async () => {
  try {
    const response = await awardAPI.listCycles({ status: 'active' })
    awardCycles.value = response.items || response
  } catch (error) {
    ElMessage.error('获取奖项轮次失败')
  }
}

const fetchOrganizations = async () => {
  try {
    const response = await organizationAPI.list({ limit: 100 })
    organizations.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    console.error('获取组织列表失败', error)
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  fetchApplications()
}

const handleReset = () => {
  searchForm.value = {
    title: '',
    applicant_unit_id: null,
    status: ''
  }
  pagination.value.page = 1
  fetchApplications()
}

const showCreateDialog = () => {
  currentEditId.value = null
  resetForm()
  dialogVisible.value = true
}

const editApplication = async (id) => {
  try {
    const data = await applicationAPI.get(id)
    currentEditId.value = id
    formData.value = { ...data }
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取申报详情失败')
  }
}

const handleSubmitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (currentEditId.value) {
          await applicationAPI.update(currentEditId.value, formData.value)
          ElMessage.success('更新成功')
        } else {
          await applicationAPI.create(formData.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchApplications()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const submitApplication = async (id) => {
  try {
    await ElMessageBox.confirm('提交后将无法修改，确认提交？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await applicationAPI.submit(id)
    ElMessage.success('提交成功')
    fetchApplications()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('提交失败')
    }
  }
}

const deleteApplication = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该申报？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await applicationAPI.delete(id)
    ElMessage.success('删除成功')
    fetchApplications()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const viewDetail = (id) => {
  router.push({ name: 'ApplicationDetail', params: { id } })
}

const resetForm = () => {
  formData.value = {
    award_cycle_id: null,
    title: '',
    category: '',
    leader_name: '',
    leader_title: '',
    team_members: '',
    summary: '',
    technical_details: '',
    innovation_points: '',
    application_value: '',
    economic_benefit: '',
    social_benefit: ''
  }
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

onMounted(() => {
  fetchApplications()
  fetchAwardCycles()
  fetchOrganizations()
})
</script>

<style scoped>
.app-container {
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
