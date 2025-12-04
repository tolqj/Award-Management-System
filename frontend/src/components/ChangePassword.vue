<template>
  <el-dialog
    v-model="dialogVisible"
    title="修改密码"
    width="450px"
    @close="resetForm"
  >
    <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
      <el-form-item label="原密码" prop="old_password">
        <el-input 
          v-model="formData.old_password" 
          type="password" 
          placeholder="请输入原密码" 
          show-password
        />
      </el-form-item>
      <el-form-item label="新密码" prop="new_password">
        <el-input 
          v-model="formData.new_password" 
          type="password" 
          placeholder="请输入新密码" 
          show-password
        />
      </el-form-item>
      <el-form-item label="确认密码" prop="confirm_password">
        <el-input 
          v-model="formData.confirm_password" 
          type="password" 
          placeholder="请再次输入新密码" 
          show-password
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/api'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const formRef = ref(null)
const submitting = ref(false)

const formData = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else if (value.length < 6) {
    callback(new Error('密码长度不能少于6位'))
  } else {
    callback()
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== formData.value.new_password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  new_password: [{ validator: validatePassword, trigger: 'blur' }],
  confirm_password: [{ validator: validateConfirmPassword, trigger: 'blur' }]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        await authAPI.changePassword({
          old_password: formData.value.old_password,
          new_password: formData.value.new_password
        })
        ElMessage.success('密码修改成功')
        dialogVisible.value = false
        resetForm()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '密码修改失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const resetForm = () => {
  formData.value = {
    old_password: '',
    new_password: '',
    confirm_password: ''
  }
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

watch(() => props.visible, (newVal) => {
  if (newVal) {
    resetForm()
  }
})
</script>
