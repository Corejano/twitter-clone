import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService, userService } from '@/services/users'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

  async function register(userData) {
    try {
      loading.value = true
      error.value = null
      const response = await authService.register(userData)

      user.value = response.user
      accessToken.value = response.tokens.access
      refreshToken.value = response.tokens.refresh

      localStorage.setItem('access_token', response.tokens.access)
      localStorage.setItem('refresh_token', response.tokens.refresh)
      localStorage.setItem('user', JSON.stringify(response.user))

      return response
    } catch (err) {
      error.value = err.response?.data || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function login(credentials) {
    try {
      loading.value = true
      error.value = null
      const response = await authService.login(credentials)

      user.value = response.user
      accessToken.value = response.tokens.access
      refreshToken.value = response.tokens.refresh

      localStorage.setItem('access_token', response.tokens.access)
      localStorage.setItem('refresh_token', response.tokens.refresh)
      localStorage.setItem('user', JSON.stringify(response.user))

      return response
    } catch (err) {
      error.value = err.response?.data || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      if (refreshToken.value) {
        await authService.logout(refreshToken.value)
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      user.value = null
      accessToken.value = null
      refreshToken.value = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }
  }

  async function fetchCurrentUser() {
    try {
      loading.value = true
      const userData = await userService.getCurrentUser()
      user.value = userData
      localStorage.setItem('user', JSON.stringify(userData))
      return userData
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch user'
      throw err
    } finally {
      loading.value = false
    }
  }

  function initializeAuth() {
    const storedUser = localStorage.getItem('user')
    if (storedUser && accessToken.value) {
      try {
        user.value = JSON.parse(storedUser)
      } catch (err) {
        console.error('Failed to parse stored user:', err)
        logout()
      }
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    isAuthenticated,
    register,
    login,
    logout,
    fetchCurrentUser,
    initializeAuth,
  }
})
