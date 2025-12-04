<template>
  <div class="committee-container">
    <el-card shadow="never">
      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="申报项目">
          <el-input 
            v-model="searchForm.title" 
            placeholder="请输入项目名称" 
            clearable 
            style="width: 220px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="决议结果">
          <el-select v-model="searchForm.decision" placeholder="全部结果" clearable style="width: 160px">
            <el-option label="通过" value="approved" />
            <el-option label="不通过" value="rejected" />
            <el-option label="需补充材料" value="pending" />
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
            <span>新增决议</span>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table 
        :data="decisions" 
        v-loading="loading" 
        stripe
        border
        style="width: 100%; margin-top: 16px;"
        :header-cell-style="headerCellStyle"
      >
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="application.title" label="申报项目" min-width="300" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="viewApplication(row.application_id)" :underline="false">
              <strong>{{ row.application?.title || '-' }}</strong>
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="decision" label="决议结果" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getResultType(row.decision)" effect="plain">
              {{ getResultText(row.decision) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="vote_for" label="赞成票" width="100" align="center">
          <template #default="{ row }">
            <el-text type="success" size="large">{{ row.vote_for || 0 }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="vote_against" label="反对票" width="100" align="center">
          <template #default="{ row }">
            <el-text type="danger" size="large">{{ row.vote_against || 0 }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="vote_abstain" label="弃权票" width="100" align="center">
          <template #default="{ row }">
            <el-text type="info" size="large">{{ row.vote_abstain || 0 }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="meeting_date" label="决议日期" width="120" align="center">
          <template #default="{ row }">
            <span style="font-size: 13px;">{{ row.meeting_date ? formatDate(row.meeting_date) : '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="decision_note" label="决议内容" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" fixed="right" width="200" align="center">
          <template #default="{ row }">
            <div style="display: flex; gap: 8px; justify-content: center;">
              <el-button size="small" type="primary" @click="viewDetail(row.id)">
                <el-icon><View /></el-icon>
                <span>查看</span>
              </el-button>
              <el-button size="small" @click="editDecision(row.id)" v-if="canEdit">
                <el-icon><Edit /></el-icon>
                <span>编辑</span>
              </el-button>
              <el-button size="small" type="danger" @click="deleteDecision(row.id)" v-if="canDelete">
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
          @size-change="fetchDecisions"
          @current-change="fetchDecisions"
          background
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="700px"
      @close="resetForm"
    >
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="申报项目" prop="application_id">
          <el-select v-model="formData.application_id" placeholder="请选择申报项目" style="width: 100%" filterable>
            <el-option
              v-for="app in applications"
              :key="app.id"
              :label="app.title"
              :value="app.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="决议结果" prop="decision">
          <el-radio-group v-model="formData.decision">
            <el-radio value="approved">通过</el-radio>
            <el-radio value="rejected">不通过</el-radio>
            <el-radio value="pending">需补充材料</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="决议日期" prop="meeting_date">
          <el-date-picker
            v-model="formData.meeting_date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="奖项等级">
          <el-input v-model="formData.award_grade" placeholder="请输入奖项等级（如：一等奖、二等奖）" />
        </el-form-item>
        <el-form-item label="投票结果">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="赞成票" prop="vote_for">
                <el-input-number v-model="formData.vote_for" :min="0" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="反对票" prop="vote_against">
                <el-input-number v-model="formData.vote_against" :min="0" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="弃权票" prop="vote_abstain">
                <el-input-number v-model="formData.vote_abstain" :min="0" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="决议内容" prop="decision_note">
          <el-input v-model="formData.decision_note" type="textarea" :rows="5" placeholder="请输入决议内容" />
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
import { View, Edit, Delete, Search, Refresh, Plus } from '@element-plus/icons-vue'
import { committeeAPI, applicationAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const decisions = ref([])
const applications = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentEditId = ref(null)

const searchForm = ref({
  title: '',
  decision: ''
})

const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

const formData = ref({
  application_id: null,
  decision: 'approved',
  decision_note: '',
  award_grade: '',
  vote_for: 0,
  vote_against: 0,
  vote_abstain: 0,
  meeting_date: ''
})

const rules = {
  application_id: [{ required: true, message: '请选择申报项目', trigger: 'change' }],
  decision: [{ required: true, message: '请选择决议结果', trigger: 'change' }],
  meeting_date: [{ required: true, message: '请选择决议日期', trigger: 'change' }],
  decision_note: [{ required: true, message: '请输入决议内容', trigger: 'blur' }]
}

const dialogTitle = computed(() => currentEditId.value ? '编辑决议' : '新增决议')
const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }
const canCreate = computed(() => ['admin', 'staff', 'committee'].includes(authStore.userRole))
const canEdit = computed(() => ['admin', 'staff'].includes(authStore.userRole))
const canDelete = computed(() => ['admin'].includes(authStore.userRole))

const getResultType = (result) => {
  const typeMap = {
    approved: 'success',
    rejected: 'danger',
    pending: 'warning'
  }
  return typeMap[result] || 'info'
}

const getResultText = (result) => {
  const textMap = {
    approved: '通过',
    rejected: '不通过',
    pending: '需补充材料'
  }
  return textMap[result] || result
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return dateStr.split(' ')[0]
}

const fetchDecisions = async () => {
  loading.value = true
  try {
    const response = await committeeAPI.listDecisions()
    if (Array.isArray(response)) {
      decisions.value = response
      pagination.value.total = response.length
    } else {
      decisions.value = response.items || []
      pagination.value.total = response.total || 0
    }
  } catch (error) {
    ElMessage.error('获取决议列表失败')
  } finally {
    loading.value = false
  }
}

const fetchApplications = async () => {
  try {
    const response = await applicationAPI.list({ status: 'expert_review' })
    applications.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    ElMessage.error('获取申报列表失败')
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  fetchDecisions()
}

const handleReset = () => {
  searchForm.value = {
    title: '',
    decision: ''
  }
  pagination.value.page = 1
  fetchDecisions()
}

const showCreateDialog = () => {
  currentEditId.value = null
  resetForm()
  dialogVisible.value = true
}

const editDecision = async (id) => {
  try {
    const data = await committeeAPI.getDecision(id)
    currentEditId.value = id
    formData.value = { ...data }
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取决议详情失败')
  }
}

const handleSubmitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (currentEditId.value) {
          await committeeAPI.updateDecision(currentEditId.value, formData.value)
          ElMessage.success('更新成功')
        } else {
          await committeeAPI.createDecision(formData.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchDecisions()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const deleteDecision = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该决议?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await committeeAPI.deleteDecision(id)
    ElMessage.success('删除成功')
    fetchDecisions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const viewDetail = (id) => {
  // 查看决议详情
  ElMessage.info('查看决议详情功能')
}

const viewApplication = (id) => {
  router.push(`/applications/${id}`)
}

const resetForm = () => {
  formData.value = {
    application_id: null,
    decision: 'approved',
    decision_note: '',
    award_grade: '',
    vote_for: 0,
    vote_against: 0,
    vote_abstain: 0,
    meeting_date: ''
  }
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

onMounted(() => {
  fetchDecisions()
  fetchApplications()
})
</script>

<style scoped>
.committee-container {
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
