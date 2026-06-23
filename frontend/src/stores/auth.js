import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isLoggedIn = ref(false)

  function setAuth(data) {
    localStorage.setItem('access_token', data.token.access)
    localStorage.setItem('refresh_token', data.token.refresh)
    user.value = { id: data.id, username: data.username, email: data.email }
    isLoggedIn.value = true
  }

  async function fetchUser() {
    try {
      const res = await authAPI.getMe()
      user.value = res.data
      isLoggedIn.value = true
    } catch {
      logout()
    }
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
    isLoggedIn.value = false
  }

  function initAuth() {
    const token = localStorage.getItem('access_token')
    if (token) {
      fetchUser()
    }
  }

  return { user, isLoggedIn, setAuth, fetchUser, logout, initAuth }
})
