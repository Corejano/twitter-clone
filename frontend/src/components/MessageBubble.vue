<template>
  <div :class="['flex mb-4', isOwnMessage ? 'justify-end' : 'justify-start']">
    <div :class="['flex max-w-[70%]', isOwnMessage ? 'flex-row-reverse' : 'flex-row']">
      <UserAvatar
        v-if="!isOwnMessage"
        :src="message.sender.avatar"
        :full-name="message.sender.full_name"
        size="sm"
        :class="isOwnMessage ? 'ml-2' : 'mr-2'"
      />

      <div>
        <div
          :class="[
            'px-4 py-2 rounded-2xl break-words',
            isOwnMessage
              ? 'bg-twitter-blue text-white rounded-br-sm'
              : 'bg-twitter-light-gray text-twitter-black rounded-bl-sm'
          ]"
        >
          <p class="whitespace-pre-wrap">{{ message.content }}</p>
        </div>

        <div :class="['flex items-center mt-1 px-2', isOwnMessage ? 'justify-end' : 'justify-start']">
          <span class="text-xs text-twitter-dark-gray">
            {{ formatTime(message.created_at) }}
          </span>
          <div v-if="isOwnMessage" class="ml-1 flex items-center">
            <svg
              v-if="message.is_read"
              :class="['w-4 h-4', message.is_read ? 'text-twitter-blue' : 'text-twitter-dark-gray']"
              fill="currentColor"
              viewBox="0 0 20 20"
              style="margin-left: -6px"
            >
              <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
            </svg>
            <svg
              :class="['w-4 h-4', message.is_read ? 'text-twitter-blue' : 'text-twitter-dark-gray']"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserAvatar from './UserAvatar.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const authStore = useAuthStore()

const isOwnMessage = computed(() => {
  return authStore.user?.id === props.message.sender.id
})

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)

  if (diffInSeconds < 60) {
    return 'just now'
  } else if (diffInSeconds < 3600) {
    return `${Math.floor(diffInSeconds / 60)}m ago`
  } else if (diffInSeconds < 86400) {
    return `${Math.floor(diffInSeconds / 3600)}h ago`
  } else if (diffInSeconds < 604800) {
    return `${Math.floor(diffInSeconds / 86400)}d ago`
  } else {
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
}
</script>
