import api from './api'

export const postService = {
  async getPosts() {
    const response = await api.get('/posts/')
    return response.data
  },

  async getPostById(postId) {
    const response = await api.get(`/posts/${postId}/`)
    return response.data
  },

  async createPost(postData) {
    const formData = new FormData()
    formData.append('content', postData.content)

    if (postData.images && postData.images.length > 0) {
      postData.images.forEach((image) => {
        formData.append('images', image)
      })
    }

    const response = await api.post('/posts/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async deletePost(postId) {
    const response = await api.delete(`/posts/${postId}/`)
    return response.data
  },

  async likePost(postId) {
    const response = await api.post(`/posts/${postId}/like/`)
    return response.data
  },

  async unlikePost(postId) {
    const response = await api.delete(`/posts/${postId}/like/`)
    return response.data
  },

  async getPostLikes(postId) {
    const response = await api.get(`/posts/${postId}/likes/`)
    return response.data
  },

  async getUserPosts(username) {
    const response = await api.get(`/users/${username}/posts/`)
    return response.data
  },

  async getUserLikedPosts(username) {
    const response = await api.get(`/users/${username}/likes/`)
    return response.data
  },
}
