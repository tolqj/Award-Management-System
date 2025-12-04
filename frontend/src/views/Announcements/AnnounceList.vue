<template>
  <div class="announce-container">
    <el-card shadow="never">
      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="公示标题">
          <el-input 
            v-model="searchForm.title" 
            placeholder="请输入公示标题" 
            clearable 
            style="width: 220px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="公示状态">
          <el-select v-model="searchForm.status" placeholder="全部状态" clearable style="width: 160px">
            <el-option label="公示中" value="active" />
            <el-option label="已结束" value="ended" />
            <el-option label="已撤销" value="cancelled" />
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
            <span>发布公示</span>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table 
        :data="announcements" 
        v-loading="loading" 
        stripe
        border
        style="width: 100%; margin-top: 16px;"
        :header-cell-style="headerCellStyle"
      >
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="title" label="公示标题" min-width="300" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="viewDetail(row.id)" :underline="false">
              <strong>{{ row.title }}</strong>
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="announcement_type" label="公示类型" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.announcement_type)" effect="plain">
              {{ getTypeText(row.announcement_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="110" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" effect="plain">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120" align="center">
          <template #default="{ row }">
            <span style="font-size: 13px;">{{ formatDate(row.start_date) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="end_date" label="结束日期" width="120" align="center">
          <template #default="{ row }">
            <span style="font-size: 13px;">{{ formatDate(row.end_date) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="objection_count" label="异议数" width="100" align="center">
          <template #default="{ row }">
            <el-text :type="row.objection_count > 0 ? 'warning' : 'info'" size="large">
              {{ row.objection_count || 0 }}
            </el-text>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170" align="center">
          <template #default="{ row }">
            <span style="font-size: 13px;">{{ formatDateTime(row.created_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="300" align="center">
          <template #default="{ row }">
            <div style="display: flex; gap: 8px; justify-content: center;">
              <el-button size="small" type="primary" @click="viewDetail(row.id)">
                <el-icon><View /></el-icon>
                <span>查看</span>
              </el-button>
              <el-button size="small" @click="viewObjections(row.id)" v-if="row.objection_count > 0">
                <el-icon><Warning /></el-icon>
                <span>异议</span>
              </el-button>
              <el-button size="small" @click="editAnnouncement(row.id)" v-if="canEdit(row)">
                <el-icon><Edit /></el-icon>
                <span>编辑</span>
              </el-button>
              <el-button size="small" type="danger" @click="cancelAnnouncement(row.id)" v-if="canCancel(row)">
                <el-icon><Close /></el-icon>
                <span>撤销</span>
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
          @size-change="fetchAnnouncements"
          @current-change="fetchAnnouncements"
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
        <el-form-item label="公示标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入公示标题" />
        </el-form-item>
        <el-form-item label="公示类型" prop="announcement_type">
          <el-radio-group v-model="formData.announcement_type">
            <el-radio label="preliminary">初审公示</el-radio>
            <el-radio label="final">终审公示</el-radio>
            <el-radio label="award">获奖公示</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="申报项目" prop="application_ids">
          <el-select 
            v-model="formData.application_ids" 
            placeholder="请选择申报项目" 
            multiple
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="app in applications"
              :key="app.id"
              :label="app.title"
              :value="app.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="公示期限" required>
          <el-col :span="11">
            <el-form-item prop="start_date">
              <el-date-picker
                v-model="formData.start_date"
                type="date"
                placeholder="开始日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align: center">至</el-col>
          <el-col :span="11">
            <el-form-item prop="end_date">
              <el-date-picker
                v-model="formData.end_date"
                type="date"
                placeholder="结束日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="公示内容" prop="content">
          <el-input v-model="formData.content" type="textarea" :rows="8" placeholder="请输入公示内容" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="formData.notes" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitForm" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 异议列表对话框 -->
    <el-dialog
      v-model="objectionDialogVisible"
      title="异议列表"
      width="900px"
    >
      <el-table :data="objections" border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="objector_name" label="异议人" width="120" />
        <el-table-column prop="objector_contact" label="联系方式" width="150" />
        <el-table-column prop="objection_content" label="异议内容" min-width="300" show-overflow-tooltip />
        <el-table-column prop="status" label="处理状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'resolved' ? 'success' : 'warning'" size="small">
              {{ row.status === 'resolved' ? '已处理' : '待处理' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="160" align="center">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { View, Edit, Delete, Search, Refresh, Plus, Warning, Close } from '@element-plus/icons-vue'
import { announcementAPI, applicationAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const announcements = ref([])
const applications = ref([])
const objections = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const objectionDialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentEditId = ref(null)

const searchForm = ref({
  title: '',
  status: ''
})

const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

const formData = ref({
  title: '',
  announcement_type: 'final',
  application_ids: [],
  start_date: '',
  end_date: '',
  content: '',
  notes: ''
})

const rules = {
  title: [{ required: true, message: '请输入公示标题', trigger: 'blur' }],
  announcement_type: [{ required: true, message: '请选择公示类型', trigger: 'change' }],
  application_ids: [{ required: true, message: '请选择申报项目', trigger: 'change' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }],
  content: [{ required: true, message: '请输入公示内容', trigger: 'blur' }]
}

const dialogTitle = computed(() => currentEditId.value ? '编辑公示' : '发布公示')
const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }
const canCreate = computed(() => ['admin', 'staff'].includes(authStore.userRole))

const canEdit = (row) => {
  return row.status === 'active' && ['admin', 'staff'].includes(authStore.userRole)
}

const canCancel = (row) => {
  return row.status === 'active' && ['admin', 'staff'].includes(authStore.userRole)
}

const getTypeColor = (type) => {
  const colorMap = {
    preliminary: 'info',
    final: 'warning',
    award: 'success'
  }
  return colorMap[type] || 'info'
}

const getTypeText = (type) => {
  const textMap = {
    preliminary: '初审公示',
    final: '终审公示',
    award: '获奖公示'
  }
  return textMap[type] || type
}

const getStatusType = (status) => {
  const typeMap = {
    active: 'success',
    ended: 'info',
    cancelled: 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    active: '公示中',
    ended: '已结束',
    cancelled: '已撤销'
  }
  return textMap[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return dateStr.split(' ')[0]
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

const fetchAnnouncements = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.value.page - 1) * pagination.value.pageSize,
      limit: pagination.value.pageSize,
      ...searchForm.value
    }
    const response = await announcementAPI.list(params)
    if (Array.isArray(response)) {
      announcements.value = response
      pagination.value.total = response.length
    } else {
      announcements.value = response.items || []
      pagination.value.total = response.total || 0
    }
  } catch (error) {
    ElMessage.error('获取公示列表失败')
  } finally {
    loading.value = false
  }
}

const fetchApplications = async () => {
  try {
    const response = await applicationAPI.list({ status: 'approved' })
    applications.value = Array.isArray(response) ? response : (response.items || [])
  } catch (error) {
    ElMessage.error('获取申报列表失败')
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  fetchAnnouncements()
}

const handleReset = () => {
  searchForm.value = {
    title: '',
    status: ''
  }
  pagination.value.page = 1
  fetchAnnouncements()
}

const showCreateDialog = () => {
  currentEditId.value = null
  resetForm()
  dialogVisible.value = true
}

const editAnnouncement = async (id) => {
  try {
    const data = await announcementAPI.get(id)
    currentEditId.value = id
    formData.value = { 
      ...data,
      application_ids: data.application_ids || []
    }
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取公示详情失败')
  }
}

const handleSubmitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (currentEditId.value) {
          await announcementAPI.update(currentEditId.value, formData.value)
          ElMessage.success('更新成功')
        } else {
          await announcementAPI.create(formData.value)
          ElMessage.success('发布成功')
        }
        dialogVisible.value = false
        fetchAnnouncements()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const cancelAnnouncement = async (id) => {
  try {
    await ElMessageBox.confirm('确认撤销该公示?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await announcementAPI.update(id, { status: 'cancelled' })
    ElMessage.success('撤销成功')
    fetchAnnouncements()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('撤销失败')
    }
  }
}

const viewObjections = async (id) => {
  try {
    objections.value = await announcementAPI.listObjections(id)
    objectionDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取异议列表失败')
  }
}

const viewDetail = (id) => {
  router.push(`/announcements/${id}`)
}

const resetForm = () => {
  formData.value = {
    title: '',
    announcement_type: 'final',
    application_ids: [],
    start_date: '',
    end_date: '',
    content: '',
    notes: ''
  }
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

onMounted(() => {
  fetchAnnouncements()
  fetchApplications()
})
</script>

<style scoped>
.announce-container {
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
