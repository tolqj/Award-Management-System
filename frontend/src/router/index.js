import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'Layout',
      component: () => import('@/views/Layout.vue'),
      redirect: '/dashboard',
      meta: { requiresAuth: true },
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/Dashboard.vue'),
          meta: { title: '仪表板' }
        },
        {
          path: 'users',
          name: 'Users',
          component: () => import('@/views/Users/UserList.vue'),
          meta: { title: '用户管理', roles: ['admin', 'staff'] }
        },
        {
          path: 'users/:id',
          name: 'UserDetail',
          component: () => import('@/views/Users/UserDetail.vue'),
          meta: { title: '用户详情', roles: ['admin', 'staff'], hideInMenu: true }
        },
        {
          path: 'organizations',
          name: 'Organizations',
          component: () => import('@/views/Organizations/OrgList.vue'),
          meta: { title: '组织管理' }
        },
        {
          path: 'organizations/:id',
          name: 'OrganizationDetail',
          component: () => import('@/views/Organizations/OrgDetail.vue'),
          meta: { title: '组织详情', hideInMenu: true }
        },
        {
          path: 'awards',
          name: 'Awards',
          component: () => import('@/views/Awards/AwardList.vue'),
          meta: { title: '奖项管理', roles: ['admin', 'staff'] }
        },
        {
          path: 'awards/:id',
          name: 'AwardDetail',
          component: () => import('@/views/Awards/AwardDetail.vue'),
          meta: { title: '奖项详情', roles: ['admin', 'staff'], hideInMenu: true }
        },
        {
          path: 'applications',
          name: 'Applications',
          component: () => import('@/views/Applications/AppList.vue'),
          meta: { title: '申报管理' }
        },
        {
          path: 'applications/:id',
          name: 'ApplicationDetail',
          component: () => import('@/views/Applications/AppDetail.vue'),
          meta: { title: '申报详情', hideInMenu: true }
        },
        {
          path: 'reviews',
          name: 'Reviews',
          component: () => import('@/views/Reviews/MyReviews.vue'),
          meta: { title: '我的评审', roles: ['expert'] }
        },
        {
          path: 'committee',
          name: 'Committee',
          component: () => import('@/views/Committee/DecisionList.vue'),
          meta: { title: '评审委员会', roles: ['admin', 'staff', 'committee'] }
        },
        {
          path: 'announcements',
          name: 'Announcements',
          component: () => import('@/views/Announcements/AnnounceList.vue'),
          meta: { title: '公示管理' }
        },
        {
          path: 'statistics',
          name: 'Statistics',
          component: () => import('@/views/Statistics.vue'),
          meta: { title: '统计分析', roles: ['admin', 'staff'] }
        },
        {
          path: 'profile',
          name: 'Profile',
          component: () => import('@/views/Profile.vue'),
          meta: { title: '个人信息', hideInMenu: true }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
