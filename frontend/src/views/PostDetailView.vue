<template>
  <div>
    <div class="border-b border-twitter-gray sticky top-0 bg-white bg-opacity-95 backdrop-blur z-10">
      <div class="flex items-center px-4 py-3">
        <button @click="$router.back()" class="mr-8 p-2 rounded-full hover:bg-twitter-light-gray">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
        </button>
        <h2 class="text-xl font-bold text-twitter-black">Post</h2>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-twitter-blue"></div>
    </div>

    <div v-else-if="post" class="p-4">
      <div class="flex items-start mb-4">
        <UserAvatar
          :src="post.author.avatar"
          :full-name="post.author.full_name"
          size="md"
          class="mr-3 cursor-pointer flex-shrink-0"
          @click="goToProfile"
        />
        <div class="flex-1 min-w-0">
          <div class="flex items-center">
            <span class="font-bold text-twitter-black hover:underline cursor-pointer" @click="goToProfile">
              {{ post.author.full_name }}
            </span>
            <svg v-if="post.author.is_verified" class="w-4 h-4 text-twitter-blue ml-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zm-1.5 14.5l-4-4 1.414-1.414L8.5 11.672l5.086-5.086L15 8l-6.5 6.5z"/>
            </svg>
          </div>
          <p class="text-twitter-dark-gray text-sm">@{{ post.author.username }}</p>
        </div>
        <button
          v-if="isOwnPost"
          @click="handleDelete"
          class="text-twitter-dark-gray hover:text-red-500 transition-colors p-2 rounded-full hover:bg-red-50"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <p class="text-twitter-black text-xl mb-4 whitespace-pre-wrap break-words">{{ post.content }}</p>

      <PostImageGallery
        v-if="post.images && post.images.length > 0"
        :images="post.images"
        class="mb-4"
      />

      <div class="flex items-center text-twitter-dark-gray text-sm mb-4 pb-4 border-b border-twitter-gray">
        <span>{{ formatFullTime(post.created_at) }}</span>
      </div>

      <div class="flex items-center pb-4 border-b border-twitter-gray">
        <button
          @click="handleLike"
          :disabled="likeLoading"
          class="flex items-center group mr-6"
        >
          <svg
            :class="[
              'w-6 h-6 transition-colors',
              post.is_liked ? 'text-pink-600 fill-current' : 'text-twitter-dark-gray group-hover:text-pink-600'
            ]"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            />
          </svg>
          <span
            :class="[
              'ml-2 transition-colors',
              post.is_liked ? 'text-pink-600 font-bold' : 'text-twitter-dark-gray group-hover:text-pink-600'
            ]"
          >
            {{ post.likes_count }}
          </span>
        </button>
      </div>
    </div>

    <div v-else class="py-20 text-center text-twitter-dark-gray">
      <p>Post not found</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import UserAvatar from '@/components/UserAvatar.vue'
import PostImageGallery from '@/components/PostImageGallery.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const postsStore = usePostsStore()

const post = ref(null)
const loading = ref(false)
const likeLoading = ref(false)

const isOwnPost = computed(() => {
  return authStore.user?.username === post.value?.author.username
})

const loadPost = async () => {
  loading.value = true
  try {
    post.value = await postsStore.fetchPostById(route.params.id)
  } catch (error) {
    console.error('Failed to load post:', error)
  } finally {
    loading.value = false
  }
}

const goToProfile = () => {
  router.push(`/users/${post.value.author.username}`)
}

const handleLike = async () => {
  if (likeLoading.value) return

  likeLoading.value = true
  try {
    const wasLiked = post.value.is_liked
    await postsStore.toggleLike(post.value.id)
    post.value.is_liked = !wasLiked
    post.value.likes_count = wasLiked ? post.value.likes_count - 1 : post.value.likes_count + 1
  } catch (error) {
    console.error('Like error:', error)
  } finally {
    likeLoading.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this post?')) return

  try {
    await postsStore.deletePost(post.value.id)
    router.push('/home')
  } catch (error) {
    console.error('Delete error:', error)
  }
}

const formatFullTime = (dateString) => {
  const date = new Date(dateString)
  const time = date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
  const dateStr = date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
  return `${time} · ${dateStr}`
}

onMounted(() => {
  loadPost()
})
</script>
