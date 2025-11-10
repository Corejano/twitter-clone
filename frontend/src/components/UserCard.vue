<template>
  <div class="flex items-start p-4 border-b border-twitter-gray hover:bg-twitter-light-gray transition-colors cursor-pointer" @click="goToProfile">
    <UserAvatar
      :src="user.avatar"
      :full-name="user.full_name"
      size="md"
      class="mr-3"
    />
    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between">
        <div class="flex-1 min-w-0">
          <div class="flex items-center">
            <span class="font-bold text-twitter-black truncate">{{ user.full_name }}</span>
            <svg v-if="user.is_verified" class="w-4 h-4 text-twitter-blue ml-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zm-1.5 14.5l-4-4 1.414-1.414L8.5 11.672l5.086-5.086L15 8l-6.5 6.5z"/>
            </svg>
          </div>
          <p class="text-twitter-dark-gray text-sm">@{{ user.username }}</p>
        </div>
        <BaseButton
          v-if="showFollowButton && !isCurrentUser"
          :variant="user.is_following ? 'outline' : 'primary'"
          size="sm"
          :loading="loading"
          @click.stop="handleFollowToggle"
        >
          {{ user.is_following ? 'Following' : 'Follow' }}
        </BaseButton>
      </div>
      <p v-if="user.bio" class="text-twitter-black mt-1 text-sm">{{ user.bio }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useProfileStore } from '@/stores/profile'
import UserAvatar from './UserAvatar.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  showFollowButton: {
    type: Boolean,
    default: true
  }
})

const router = useRouter()
const authStore = useAuthStore()
const profileStore = useProfileStore()
const loading = ref(false)

const isCurrentUser = computed(() => {
  return authStore.user?.username === props.user.username
})

const goToProfile = () => {
  router.push(`/users/${props.user.username}`)
}

const handleFollowToggle = async () => {
  loading.value = true
  try {
    if (props.user.is_following) {
      await profileStore.unfollowUser(props.user.username)
      props.user.is_following = false
    } else {
      await profileStore.followUser(props.user.username)
      props.user.is_following = true
    }
  } catch (error) {
    console.error('Follow toggle error:', error)
  } finally {
    loading.value = false
  }
}
</script>
