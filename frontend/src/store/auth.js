import { defineStore } from 'pinia'
import { authAPI } from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null
  },
  
  actions: {
    async login(credentials) {
      try {
        const response = await authAPI.login(credentials)
        this.token = response.access_token
        localStorage.setItem('token', response.access_token)
        await this.fetchUser()
        return true
      } catch (error) {
        return false
      }
    },
    
    async fetchUser() {
      try {
        const user = await authAPI.getMe()
        this.user = user
        localStorage.setItem('user', JSON.stringify(user))
      } catch (error) {
        this.logout()
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})
