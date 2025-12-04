<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <div class="logo">
        <h3>XXXX协会</h3>
      </div>
      <el-menu :default-active="$route.path" router>
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表板</span>
        </el-menu-item>
        <el-menu-item index="/applications" v-if="canAccess(['admin', 'staff', 'applicant'])">
          <el-icon><Document /></el-icon>
          <span>申报管理</span>
        </el-menu-item>
        <el-menu-item index="/reviews" v-if="canAccess(['expert'])">
          <el-icon><Edit /></el-icon>
          <span>我的评审</span>
        </el-menu-item>
        <el-menu-item index="/committee" v-if="canAccess(['admin', 'staff', 'committee'])">
          <el-icon><Stamp /></el-icon>
          <span>评审委员会</span>
        </el-menu-item>
        <el-menu-item index="/announcements">
          <el-icon><Bell /></el-icon>
          <span>公示管理</span>
        </el-menu-item>
        <el-menu-item index="/users" v-if="canAccess(['admin', 'staff'])">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/organizations" v-if="canAccess(['admin', 'staff'])">
          <el-icon><OfficeBuilding /></el-icon>
          <span>组织管理</span>
        </el-menu-item>
        <el-menu-item index="/awards" v-if="canAccess(['admin', 'staff'])">
          <el-icon><Trophy /></el-icon>
          <span>奖项管理</span>
        </el-menu-item>
        <el-menu-item index="/statistics" v-if="canAccess(['admin', 'staff'])">
          <el-icon><PieChart /></el-icon>
          <span>统计分析</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div class="header-title">{{ $route.meta.title || 'XXXX协会科学技术奖评审管理系统' }}</div>
        <div class="header-right">
          <span class="user-name">{{ authStore.user?.real_name }}</span>
          <el-dropdown>
            <el-icon><Setting /></el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="goToProfile">
                  <el-icon><User /></el-icon>
                  <span>个人信息</span>
                </el-dropdown-item>
                <el-dropdown-item @click="showChangePassword">
                  <el-icon><Lock /></el-icon>
                  <span>修改密码</span>
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  <span>退出登录</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>

    <!-- 修改密码对话框 -->
    <ChangePassword v-model:visible="passwordDialogVisible" />
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  DataAnalysis, Document, Edit, Stamp, Bell, User, OfficeBuilding, 
  Trophy, PieChart, Setting, Lock, SwitchButton 
} from '@element-plus/icons-vue'
import ChangePassword from '@/components/ChangePassword.vue'

const router = useRouter()
const authStore = useAuthStore()
const passwordDialogVisible = ref(false)

onMounted(async () => {
  if (!authStore.user && authStore.token) {
    await authStore.fetchUser()
  }
})

const canAccess = (roles) => {
  return roles.includes(authStore.userRole)
}

const goToProfile = () => {
  router.push('/profile')
}

const showChangePassword = () => {
  passwordDialogVisible.value = true
}

const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-aside {
  background-color: #304156;
  color: #fff;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2c3e50;
}

.logo h3 {
  margin: 0;
  font-size: 18px;
  color: #fff;
}

.el-menu {
  border-right: none;
  background-color: #304156;
}

.el-menu-item {
  color: rgba(255, 255, 255, 0.7);
}

.el-menu-item:hover {
  background-color: #263445 !important;
  color: #fff;
}

.el-menu-item.is-active {
  background-color: #409eff !important;
  color: #fff;
}

.el-header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-name {
  font-size: 14px;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
