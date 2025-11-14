<template>
  <div>
    <div class="border-b border-twitter-gray sticky top-0 bg-white bg-opacity-95 backdrop-blur z-10">
      <div class="flex items-center px-4 py-3">
        <button @click="$router.back()" class="mr-8 p-2 rounded-full text-black hover:bg-twitter-light-gray">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
        </button>
        <div>
          <h2 class="text-xl font-bold text-twitter-black">{{ profile?.full_name }}</h2>
          <p class="text-sm text-twitter-dark-gray">{{ profile?.posts_count || 0 }} posts</p>
        </div>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="text-twitter-dark-gray">Loading...</div>
    </div>

    <div v-else-if="profile">
      <div class="relative">
        <div class="h-48 bg-twitter-gray">
          <img
            v-if="profile.header_image"
            :src="profile.header_image"
            alt="Header"
            class="w-full h-full object-cover"
          />
        </div>

        <div class="px-4">
          <div class="flex justify-between items-start -mt-16 mb-4">
            <UserAvatar
              :src="profile.avatar"
              :full-name="profile.full_name"
              size="xl"
              class="border-4 border-white"
            />

            <div class="mt-20">
              <BaseButton
                v-if="isCurrentUser"
                variant="outline"
                @click="goToEditProfile"
              >
                Edit profile
              </BaseButton>
              <BaseButton
                v-else
                :variant="profile.is_following ? 'outline' : 'primary'"
                :loading="followLoading"
                @click="handleFollowToggle"
              >
                {{ profile.is_following ? 'Following' : 'Follow' }}
              </BaseButton>
            </div>
          </div>

          <div class="mb-4">
            <div class="flex items-center">
              <h2 class="text-xl font-bold text-twitter-black">{{ profile.full_name }}</h2>
              <svg v-if="profile.is_verified" class="w-5 h-5 text-twitter-blue ml-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zm-1.5 14.5l-4-4 1.414-1.414L8.5 11.672l5.086-5.086L15 8l-6.5 6.5z"/>
              </svg>
            </div>
            <p class="text-twitter-dark-gray">@{{ profile.username }}</p>
          </div>

          <p v-if="profile.bio" class="text-twitter-black mb-4">{{ profile.bio }}</p>

          <div class="flex items-center text-twitter-dark-gray text-sm mb-4">
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            Joined {{ formatDate(profile.date_joined) }}
          </div>

          <div class="flex space-x-4 mb-4">
            <button @click="goToFollowing" class="hover:underline">
              <span class="font-bold text-twitter-black">{{ profile.following_count }}</span>
              <span class="text-twitter-dark-gray ml-1">Following</span>
            </button>
            <button @click="goToFollowers" class="hover:underline">
              <span class="font-bold text-twitter-black">{{ profile.followers_count }}</span>
              <span class="text-twitter-dark-gray ml-1">Followers</span>
            </button>
          </div>
        </div>
      </div>

      <div class="border-t border-twitter-gray">
        <div class="flex">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            @click="activeTab = tab.value"
            :class="[
              'flex-1 py-4 text-center font-semibold transition-colors',
              activeTab === tab.value
                ? 'text-twitter-black border-b-4 border-twitter-blue'
                : 'text-twitter-dark-gray hover:bg-twitter-light-gray'
            ]"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <div class="min-h-screen">
        <div v-if="loadingPosts" class="py-12 text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-twitter-blue"></div>
        </div>

        <div v-else-if="currentPosts.length === 0" class="py-12 text-center text-twitter-dark-gray">
          <p>{{ activeTab === 'posts' ? 'No posts yet' : 'No likes yet' }}</p>
        </div>

        <div v-else>
          <PostCard
            v-for="post in currentPosts"
            :key="post.id"
            :post="post"
            @deleted="handlePostDeleted"
            @liked="handlePostLiked"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useProfileStore } from '@/stores/profile'
import { usePostsStore } from '@/stores/posts'
import UserAvatar from '@/components/UserAvatar.vue'
import BaseButton from '@/components/BaseButton.vue'
import PostCard from '@/components/PostCard.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const profileStore = useProfileStore()
const postsStore = usePostsStore()

const profile = computed(() => profileStore.currentProfile)
const loading = ref(false)
const followLoading = ref(false)
const loadingPosts = ref(false)
const activeTab = ref('posts')
const userPosts = ref([])
const likedPosts = ref([])

const tabs = [
  { label: 'Posts', value: 'posts' },
  { label: 'Likes', value: 'likes' }
]

const isCurrentUser = computed(() => {
  return authStore.user?.username === profile.value?.username
})

const currentPosts = computed(() => {
  return activeTab.value === 'posts' ? userPosts.value : likedPosts.value
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
}

const loadProfile = async () => {
  loading.value = true
  try {
    await profileStore.fetchProfile(route.params.username)
  } catch (error) {
    console.error('Failed to load profile:', error)
  } finally {
    loading.value = false
  }
}

const handleFollowToggle = async () => {
  followLoading.value = true
  try {
    if (profile.value.is_following) {
      await profileStore.unfollowUser(profile.value.username)
    } else {
      await profileStore.followUser(profile.value.username)
    }
    await loadProfile()
  } catch (error) {
    console.error('Follow toggle error:', error)
  } finally {
    followLoading.value = false
  }
}

const goToEditProfile = () => {
  router.push('/settings/profile')
}

const goToFollowers = () => {
  router.push(`/users/${profile.value.username}/followers`)
}

const goToFollowing = () => {
  router.push(`/users/${profile.value.username}/following`)
}

const loadUserPosts = async () => {
  if (!profile.value?.username) return

  loadingPosts.value = true
  try {
    userPosts.value = await postsStore.fetchUserPosts(profile.value.username)
  } catch (error) {
    console.error('Failed to load user posts:', error)
  } finally {
    loadingPosts.value = false
  }
}

const loadLikedPosts = async () => {
  if (!profile.value?.username) return

  loadingPosts.value = true
  try {
    likedPosts.value = await postsStore.fetchUserLikedPosts(profile.value.username)
  } catch (error) {
    console.error('Failed to load liked posts:', error)
  } finally {
    loadingPosts.value = false
  }
}

const handlePostDeleted = (postId) => {
  userPosts.value = userPosts.value.filter(post => post.id !== postId)
  likedPosts.value = likedPosts.value.filter(post => post.id !== postId)
}

const handlePostLiked = ({ postId, isLiked }) => {
  const updatePost = (post) => {
    if (post.id === postId) {
      post.is_liked = isLiked
      post.likes_count = isLiked ? post.likes_count + 1 : post.likes_count - 1
    }
  }

  userPosts.value.forEach(updatePost)
  likedPosts.value.forEach(updatePost)
}

watch(() => route.params.username, async () => {
  if (route.params.username) {
    userPosts.value = []
    likedPosts.value = []
    activeTab.value = 'posts'
    await loadProfile()
    await loadUserPosts()
  }
})

watch(activeTab, async (newTab, oldTab) => {
  if (newTab === 'posts' && userPosts.value.length === 0) {
    await loadUserPosts()
  } else if (newTab === 'likes' && likedPosts.value.length === 0) {
    await loadLikedPosts()
  }
})

onMounted(async () => {
  await loadProfile()
  await loadUserPosts()
})
</script>
