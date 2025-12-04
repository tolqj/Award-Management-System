<template>
  <div class="org-container">
    <el-card shadow="never">
      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="组织名称">
          <el-input 
            v-model="searchForm.name" 
            placeholder="请输入组织名称" 
            clearable 
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="组织类型">
          <el-select v-model="searchForm.org_type" placeholder="全部类型" clearable style="width: 160px">
            <el-option label="企业" value="enterprise" />
            <el-option label="高校" value="university" />
            <el-option label="科研院所" value="research_institute" />
            <el-option label="推荐单位" value="recommender" />
            <el-option label="其他" value="other" />
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
            <span>新增组织</span>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table 
        :data="organizations" 
        v-loading="loading" 
        stripe
        border
        style="width: 100%; margin-top: 16px;"
        :header-cell-style="headerCellStyle"
      >
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="name" label="组织名称" min-width="250" show-overflow-tooltip>
          <template #default="{ row }">
            <strong>{{ row.name }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="code" label="组织代码" width="150" align="center" />
        <el-table-column prop="org_type" label="组织类型" width="130" align="center">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.org_type)" effect="plain">
              {{ getTypeText(row.org_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="contact_person" label="联系人" width="110" align="center" />
        <el-table-column prop="contact_phone" label="联系电话" width="140" align="center" />
        <el-table-column prop="email" label="邮箱" width="200" show-overflow-tooltip />
        <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
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
              <el-button size="small" @click="editOrganization(row.id)" v-if="canEdit">
                <el-icon><Edit /></el-icon>
                <span>编辑</span>
              </el-button>
              <el-button size="small" type="danger" @click="deleteOrganization(row.id)" v-if="canDelete">
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
          @size-change="fetchOrganizations"
          @current-change="fetchOrganizations"
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
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="组织名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入组织名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="组织代码" prop="code">
              <el-input v-model="formData.code" placeholder="请输入组织代码" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="组织类型" prop="org_type">
          <el-select v-model="formData.org_type" placeholder="请选择组织类型" style="width: 100%">
            <el-option label="企业" value="enterprise" />
            <el-option label="高校" value="university" />
            <el-option label="科研院所" value="research_institute" />
            <el-option label="推荐单位" value="recommender" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系人" prop="contact_person">
              <el-input v-model="formData.contact_person" placeholder="请输入联系人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contact_phone">
              <el-input v-model="formData.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="formData.address" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="4" placeholder="请输入组织描述" />
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
import { organizationAPI } from '@/api'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const organizations = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const currentEditId = ref(null)

const searchForm = ref({
  name: '',
  org_type: ''
})

const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

const formData = ref({
  name: '',
  code: '',
  org_type: '',
  contact_person: '',
  contact_phone: '',
  email: '',
  address: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入组织名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入组织代码', trigger: 'blur' }],
  org_type: [{ required: true, message: '请选择组织类型', trigger: 'change' }],
  contact_person: [{ required: true, message: '请输入联系人', trigger: 'blur' }],
  contact_phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  email: [{ type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }]
}

const dialogTitle = computed(() => currentEditId.value ? '编辑组织' : '新增组织')
const headerCellStyle = { background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }
const canCreate = computed(() => ['admin', 'staff'].includes(authStore.userRole))
const canEdit = computed(() => ['admin', 'staff'].includes(authStore.userRole))
const canDelete = computed(() => authStore.userRole === 'admin')

const getTypeColor = (type) => {
  const colorMap = {
    enterprise: 'primary',
    university: 'success',
    research_institute: 'warning',
    recommender: 'danger',
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
    other: '其他'
  }
  return textMap[type] || type
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

const fetchOrganizations = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.value.page - 1) * pagination.value.pageSize,
      limit: pagination.value.pageSize,
      ...searchForm.value
    }
    const response = await organizationAPI.list(params)
    if (Array.isArray(response)) {
      organizations.value = response
      pagination.value.total = response.length
    } else {
      organizations.value = response.items || []
      pagination.value.total = response.total || 0
    }
  } catch (error) {
    ElMessage.error('获取组织列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  fetchOrganizations()
}

const handleReset = () => {
  searchForm.value = {
    name: '',
    org_type: ''
  }
  pagination.value.page = 1
  fetchOrganizations()
}

const showCreateDialog = () => {
  currentEditId.value = null
  resetForm()
  dialogVisible.value = true
}

const editOrganization = async (id) => {
  try {
    const data = await organizationAPI.get(id)
    currentEditId.value = id
    formData.value = { ...data }
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取组织详情失败')
  }
}

const handleSubmitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (currentEditId.value) {
          await organizationAPI.update(currentEditId.value, formData.value)
          ElMessage.success('更新成功')
        } else {
          await organizationAPI.create(formData.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchOrganizations()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const deleteOrganization = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该组织?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await organizationAPI.delete(id)
    ElMessage.success('删除成功')
    fetchOrganizations()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const viewDetail = (id) => {
  router.push({ name: 'OrganizationDetail', params: { id } })
}

const resetForm = () => {
  formData.value = {
    name: '',
    code: '',
    org_type: '',
    contact_person: '',
    contact_phone: '',
    email: '',
    address: '',
    description: ''
  }
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

onMounted(() => {
  fetchOrganizations()
})
</script>

<style scoped>
.org-container {
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
