import { defineStore } from 'pinia'
import { ref } from 'vue'
import { postService } from '@/services/posts'

export const usePostsStore = defineStore('posts', () => {
  const posts = ref([])
  const currentPost = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchPosts() {
    try {
      loading.value = true
      error.value = null
      const response = await postService.getPosts()
      posts.value = response.results || response
      return posts.value
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch posts'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchPostById(postId) {
    try {
      loading.value = true
      error.value = null
      const post = await postService.getPostById(postId)
      currentPost.value = post
      return post
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch post'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createPost(postData) {
    try {
      loading.value = true
      error.value = null
      const newPost = await postService.createPost(postData)
      posts.value.unshift(newPost)
      return newPost
    } catch (err) {
      error.value = err.response?.data || 'Failed to create post'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deletePost(postId) {
    try {
      loading.value = true
      error.value = null
      await postService.deletePost(postId)
      posts.value = posts.value.filter(post => post.id !== postId)
    } catch (err) {
      error.value = err.response?.data || 'Failed to delete post'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function likePost(postId) {
    try {
      await postService.likePost(postId)
      const post = posts.value.find(p => p.id === postId)
      if (post) {
        post.is_liked = true
        post.likes_count++
      }
      if (currentPost.value?.id === postId) {
        currentPost.value.is_liked = true
        currentPost.value.likes_count++
      }
    } catch (err) {
      error.value = err.response?.data || 'Failed to like post'
      throw err
    }
  }

  async function unlikePost(postId) {
    try {
      await postService.unlikePost(postId)
      const post = posts.value.find(p => p.id === postId)
      if (post) {
        post.is_liked = false
        post.likes_count--
      }
      if (currentPost.value?.id === postId) {
        currentPost.value.is_liked = false
        currentPost.value.likes_count--
      }
    } catch (err) {
      error.value = err.response?.data || 'Failed to unlike post'
      throw err
    }
  }

  async function toggleLike(postId) {
    const post = posts.value.find(p => p.id === postId) || currentPost.value
    if (post?.is_liked) {
      await unlikePost(postId)
    } else {
      await likePost(postId)
    }
  }

  async function fetchUserPosts(username) {
    try {
      loading.value = true
      error.value = null
      const userPosts = await postService.getUserPosts(username)
      return userPosts
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch user posts'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchUserLikedPosts(username) {
    try {
      loading.value = true
      error.value = null
      const likedPosts = await postService.getUserLikedPosts(username)
      return likedPosts
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch liked posts'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearPosts() {
    posts.value = []
    currentPost.value = null
  }

  return {
    posts,
    currentPost,
    loading,
    error,
    fetchPosts,
    fetchPostById,
    createPost,
    deletePost,
    likePost,
    unlikePost,
    toggleLike,
    fetchUserPosts,
    fetchUserLikedPosts,
    clearPosts,
  }
})
