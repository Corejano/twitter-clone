import { defineStore } from 'pinia'
import { ref } from 'vue'
import { userService } from '@/services/users'

export const useProfileStore = defineStore('profile', () => {
  const currentProfile = ref(null)
  const followers = ref([])
  const following = ref([])
  const searchResults = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchProfile(username) {
    try {
      loading.value = true
      error.value = null
      const profile = await userService.getUserByUsername(username)
      currentProfile.value = profile
      return profile
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchFollowers(username) {
    try {
      loading.value = true
      error.value = null
      const followersList = await userService.getFollowers(username)
      followers.value = followersList
      return followersList
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch followers'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchFollowing(username) {
    try {
      loading.value = true
      error.value = null
      const followingList = await userService.getFollowing(username)
      following.value = followingList
      return followingList
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch following'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function followUser(username) {
    try {
      await userService.followUser(username)
      if (currentProfile.value && currentProfile.value.username === username) {
        currentProfile.value.is_following = true
        currentProfile.value.followers_count += 1
      }
    } catch (err) {
      error.value = err.response?.data || 'Failed to follow user'
      throw err
    }
  }

  async function unfollowUser(username) {
    try {
      await userService.unfollowUser(username)
      if (currentProfile.value && currentProfile.value.username === username) {
        currentProfile.value.is_following = false
        currentProfile.value.followers_count -= 1
      }
    } catch (err) {
      error.value = err.response?.data || 'Failed to unfollow user'
      throw err
    }
  }

  async function searchUsers(query) {
    try {
      loading.value = true
      error.value = null
      const results = await userService.searchUsers(query)
      searchResults.value = results
      return results
    } catch (err) {
      error.value = err.response?.data || 'Failed to search users'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearProfile() {
    currentProfile.value = null
    followers.value = []
    following.value = []
  }

  function clearSearch() {
    searchResults.value = []
  }

  return {
    currentProfile,
    followers,
    following,
    searchResults,
    loading,
    error,
    fetchProfile,
    fetchFollowers,
    fetchFollowing,
    followUser,
    unfollowUser,
    searchUsers,
    clearProfile,
    clearSearch,
  }
})
