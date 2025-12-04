<template>
  <div class="award-container">
    <el-card shadow="never">
      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="奖项名称">
          <el-input 
            v-model="searchForm.name" 
            placeholder="请输入奖项名称" 
            clearable 
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
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
            <span>新增奖项</span>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table 
        :data="awards" 
        v-loading="loading" 
        stripe
        border
        style="width: 100%; margin-top: 16px;"
        :header-cell-style="headerCellStyle"
      >
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="name" label="奖项名称" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <strong>{{ row.name }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="奖项类别" width="150" align="center" />
        <el-table-column prop="level" label="奖项等级" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="getLevelType(row.level)" effect="plain">
              {{ getLevelText(row.level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quota" label="名额限制" width="100" align="center" />
        <el-table-column prop="bonus_amount" label="奖金(元)" width="120" align="center">
          <template #default="{ row }">
            <el-text type="success" size="large">{{ row.bonus_amount || 0 }}</el-text>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="170" align="center">
          <template #default="{ row }">
            <span style="font-size: 13px;">{{ formatDateTime(row.created_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="240" align="center">
          <template #default="{ row }">
            <div style="display: flex; gap: 8px; justify-content: center;">
              <el-button size="small" type="primary" @click="viewDetail(row.id)">
                <el-icon><View /></el-icon>
                <span>查看</span>
              </el-button>
              <el-button size="small" @click="editAward(row.id)" v-if="canEdit">
                <el-icon><Edit /></el-icon>
                <span>编辑</span>
              </el-button>
              <el-button size="small" type="danger" @click="deleteAward(row.id)" v-if="canDelete">
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
          @size-change="fetchAwards"
          @current-change="fetchAwards"
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
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="奖项名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入奖项名称" />
        </el-form-item>
        <el-form-item label="奖项类别" prop="category">
          <el-input v-model="formData.category" placeholder="请输入奖项类别" />
        </el-form-item>
        <el-form-item label="奖项等级" prop="level">
          <el-select v-model="formData.level" placeholder="请选择奖项等级" style="width: 100%">
            <el-option label="特等奖" value="special" />
            <el-option label="一等奖" value="first" />
            <el-option label="二等奖" value="second" />
            <el-option label="三等奖" value="third" />
          </el-select>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="名额限制" prop="quota">
              <el-input-number v-model="formData.quota" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="奖金(元)" prop="bonus_amount">
              <el-input-number v-model="formData.bonus_amount" :min="0" :step="1000" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="评审标准">
          <el-input v-model="formData.criteria" type="textarea" :rows="4" placeholder="请输入评审标准" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入奖项描述" />
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
import { awardAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const awards = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentEditId = ref(null)

const searchForm = ref({
  name: ''
})

const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

const formData = ref({
  name: '',
  category: '',
  level: '',
  quota: 1,
  bonus_amount: 0,
  criteria: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入奖项名称', trigger: 'blur' }],
  category: [{ required: true, message: '请输入奖项类别', trigger: 'blur' }],
  level: [{ required: true, message: '请选择奖项等级', trigger: 'change' }],
  quota: [{ required: true, message: '请输入名额限制', trigger: 'blur' }]
}

const dialogTitle = computed(() => currentEditId.value ? '编辑奖项' : '新增奖项')
const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }
const canCreate = computed(() => ['admin', 'staff'].includes(authStore.userRole))
const canEdit = computed(() => ['admin', 'staff'].includes(authStore.userRole))
const canDelete = computed(() => authStore.userRole === 'admin')

const getLevelType = (level) => {
  const typeMap = {
    special: 'danger',
    first: 'warning',
    second: 'success',
    third: 'info'
  }
  return typeMap[level] || 'info'
}

const getLevelText = (level) => {
  const textMap = {
    special: '特等奖',
    first: '一等奖',
    second: '二等奖',
    third: '三等奖'
  }
  return textMap[level] || level
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

const fetchAwards = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.value.page - 1) * pagination.value.pageSize,
      limit: pagination.value.pageSize,
      ...searchForm.value
    }
    const response = await awardAPI.list(params)
    if (Array.isArray(response)) {
      awards.value = response
      pagination.value.total = response.length
    } else {
      awards.value = response.items || []
      pagination.value.total = response.total || 0
    }
  } catch (error) {
    ElMessage.error('获取奖项列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  fetchAwards()
}

const handleReset = () => {
  searchForm.value = { name: '' }
  pagination.value.page = 1
  fetchAwards()
}

const showCreateDialog = () => {
  currentEditId.value = null
  resetForm()
  dialogVisible.value = true
}

const editAward = async (id) => {
  try {
    const data = await awardAPI.get(id)
    currentEditId.value = id
    formData.value = { ...data }
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取奖项详情失败')
  }
}

const handleSubmitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (currentEditId.value) {
          await awardAPI.update(currentEditId.value, formData.value)
          ElMessage.success('更新成功')
        } else {
          await awardAPI.create(formData.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchAwards()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const deleteAward = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该奖项？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await awardAPI.delete(id)
    ElMessage.success('删除成功')
    fetchAwards()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const viewDetail = (id) => {
  router.push({ name: 'AwardDetail', params: { id } })
}

const resetForm = () => {
  formData.value = {
    name: '',
    category: '',
    level: '',
    quota: 1,
    bonus_amount: 0,
    criteria: '',
    description: ''
  }
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

onMounted(() => {
  fetchAwards()
})
</script>

<style scoped>
.award-container {
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
