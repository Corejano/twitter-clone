<template>
  <div class="flex p-4 border-b border-twitter-gray hover:bg-twitter-light-gray transition-colors cursor-pointer" @click="goToPost">
    <UserAvatar
      :src="post.author.avatar"
      :full-name="post.author.full_name"
      size="md"
      class="mr-3 cursor-pointer flex-shrink-0"
      @click.stop="goToProfile"
    />
    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between">
        <div class="flex items-center min-w-0 flex-1">
          <span class="font-bold text-twitter-black hover:underline truncate" @click.stop="goToProfile">
            {{ post.author.full_name }}
          </span>
          <svg v-if="post.author.is_verified" class="w-4 h-4 text-twitter-blue ml-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zm-1.5 14.5l-4-4 1.414-1.414L8.5 11.672l5.086-5.086L15 8l-6.5 6.5z"/>
          </svg>
          <span class="text-twitter-dark-gray text-sm ml-1 truncate">@{{ post.author.username }}</span>
          <span class="text-twitter-dark-gray mx-1">·</span>
          <span class="text-twitter-dark-gray text-sm flex-shrink-0">{{ formatTime(post.created_at) }}</span>
        </div>
        <button
          v-if="isOwnPost"
          @click.stop="handleDelete"
          class="text-twitter-dark-gray hover:text-red-500 transition-colors p-2 rounded-full hover:bg-red-50"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <p class="text-twitter-black mt-2 whitespace-pre-wrap break-words">{{ post.content }}</p>

      <PostImageGallery
        v-if="post.images && post.images.length > 0"
        :images="post.images"
        class="mt-3"
      />

      <div class="flex items-center mt-3 -ml-2" @click.stop>
        <button
          @click="handleLike"
          :disabled="likeLoading"
          class="flex items-center group p-2 rounded-full hover:bg-pink-50 transition-colors"
        >
          <svg
            :class="[
              'w-5 h-5 transition-colors',
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
              'ml-2 text-sm transition-colors',
              post.is_liked ? 'text-pink-600' : 'text-twitter-dark-gray group-hover:text-pink-600'
            ]"
          >
            {{ post.likes_count }}
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import UserAvatar from './UserAvatar.vue'
import PostImageGallery from './PostImageGallery.vue'

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['deleted', 'liked'])

const router = useRouter()
const authStore = useAuthStore()
const postsStore = usePostsStore()
const likeLoading = ref(false)

const isOwnPost = computed(() => {
  return authStore.user?.username === props.post.author.username
})

const goToProfile = () => {
  router.push(`/users/${props.post.author.username}`)
}

const goToPost = () => {
  router.push(`/posts/${props.post.id}`)
}

const handleLike = async () => {
  if (likeLoading.value) return

  likeLoading.value = true
  try {
    const wasLiked = props.post.is_liked
    await postsStore.toggleLike(props.post.id)
    emit('liked', { postId: props.post.id, isLiked: !wasLiked })
  } catch (error) {
    console.error('Like error:', error)
  } finally {
    likeLoading.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this post?')) return

  try {
    await postsStore.deletePost(props.post.id)
    emit('deleted', props.post.id)
  } catch (error) {
    console.error('Delete error:', error)
  }
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)

  if (diffInSeconds < 60) {
    return `${diffInSeconds}s`
  } else if (diffInSeconds < 3600) {
    return `${Math.floor(diffInSeconds / 60)}m`
  } else if (diffInSeconds < 86400) {
    return `${Math.floor(diffInSeconds / 3600)}h`
  } else if (diffInSeconds < 604800) {
    return `${Math.floor(diffInSeconds / 86400)}d`
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }
}
</script>
