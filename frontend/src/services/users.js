import api from './api'

export const authService = {
  async register(userData) {
    const response = await api.post('/auth/register/', userData)
    return response.data
  },

  async login(credentials) {
    const response = await api.post('/auth/login/', credentials)
    return response.data
  },

  async logout(refreshToken) {
    const response = await api.post('/auth/logout/', { refresh: refreshToken })
    return response.data
  },
}

export const userService = {
  async getCurrentUser() {
    const response = await api.get('/users/me/')
    return response.data
  },

  async updateCurrentUser(userData) {
    const formData = new FormData()

    Object.keys(userData).forEach(key => {
      if (userData[key] !== null && userData[key] !== undefined) {
        formData.append(key, userData[key])
      }
    })

    const response = await api.patch('/users/update_me/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async getUserByUsername(username) {
    const response = await api.get(`/users/${username}/`)
    return response.data
  },

  async getFollowers(username) {
    const response = await api.get(`/users/${username}/followers/`)
    return response.data
  },

  async getFollowing(username) {
    const response = await api.get(`/users/${username}/following/`)
    return response.data
  },

  async followUser(username) {
    const response = await api.post(`/users/${username}/follow/`)
    return response.data
  },

  async unfollowUser(username) {
    const response = await api.delete(`/users/${username}/unfollow/`)
    return response.data
  },

  async searchUsers(query) {
    const response = await api.get('/users/search/', {
      params: { q: query },
    })
    return response.data
  },
}
