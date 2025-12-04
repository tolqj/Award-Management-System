<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>XXXX协会科学技术奖</h2>
        <p>评审管理系统</p>
      </div>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入用户名"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            @click="handleLogin" 
            :loading="loading"
            size="large"
            style="width: 100%"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <div class="demo-accounts">
        <p>演示账号:</p>
        <p>管理员: admin / admin123</p>
        <p>工作人员: staff01 / staff123</p>
        <p>专家: expert01 / expert123</p>
        <p>申报人: applicant01 / app123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      const formData = new FormData()
      formData.append('username', loginForm.value.username)
      formData.append('password', loginForm.value.password)
      
      const success = await authStore.login(formData)
      loading.value = false
      
      if (success) {
        ElMessage.success('登录成功')
        router.push('/')
      } else {
        ElMessage.error('登录失败,请检查用户名和密码')
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 5px;
}

.login-header p {
  font-size: 16px;
  color: #666;
}

.login-form {
  margin-top: 30px;
}

.demo-accounts {
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 5px;
  font-size: 12px;
  color: #666;
}

.demo-accounts p {
  margin: 5px 0;
}
</style>
