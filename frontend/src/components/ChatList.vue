<template>
  <div class="flex flex-col h-full">
    <div class="border-b border-twitter-gray p-4 flex items-center justify-between">
      <h2 class="text-xl font-bold text-twitter-black">Messages</h2>
      <button
        @click="$emit('new-chat')"
        class="p-2 rounded-full hover:bg-twitter-light-gray transition-colors"
      >
        <svg class="w-6 h-6 text-twitter-blue" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>

    <div v-if="loading && chats.length === 0" class="flex-1 flex items-center justify-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-twitter-blue"></div>
    </div>

    <div v-else-if="chats.length === 0" class="flex-1 flex flex-col items-center justify-center p-8 text-center">
      <svg class="w-16 h-16 text-twitter-dark-gray mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
      <h3 class="text-xl font-bold text-twitter-black mb-2">No messages yet</h3>
      <p class="text-twitter-dark-gray mb-4">Start a conversation with someone</p>
      <BaseButton @click="$emit('new-chat')" variant="primary" size="md">
        New Message
      </BaseButton>
    </div>

    <div v-else class="flex-1 overflow-y-auto">
      <div
        v-for="chat in chats"
        :key="chat.id"
        @click="$emit('select-chat', chat)"
        :class="[
          'flex items-center p-4 border-b border-twitter-gray hover:bg-twitter-light-gray transition-colors cursor-pointer',
          selectedChatId === chat.id ? 'bg-twitter-light-gray' : ''
        ]"
      >
        <div class="relative mr-3">
          <UserAvatar
            :src="chat.other_participant?.avatar"
            :full-name="chat.other_participant?.full_name"
            size="md"
          />
          <div
            v-if="chat.unread_count > 0"
            class="absolute -top-1 -right-1 bg-twitter-blue text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center"
          >
            {{ chat.unread_count > 9 ? '9+' : chat.unread_count }}
          </div>
        </div>

        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-1">
            <div class="flex items-center min-w-0 flex-1">
              <span class="font-bold text-twitter-black truncate">
                {{ chat.other_participant?.full_name }}
              </span>
              <svg
                v-if="chat.other_participant?.is_verified"
                class="w-4 h-4 text-twitter-blue ml-1 flex-shrink-0"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zm-1.5 14.5l-4-4 1.414-1.414L8.5 11.672l5.086-5.086L15 8l-6.5 6.5z"/>
              </svg>
              <span class="text-twitter-dark-gray text-sm ml-1 truncate">
                @{{ chat.other_participant?.username }}
              </span>
            </div>
            <span class="text-xs text-twitter-dark-gray flex-shrink-0 ml-2">
              {{ formatTime(chat.last_message?.created_at || chat.updated_at) }}
            </span>
          </div>

          <p
            :class="[
              'text-sm truncate',
              chat.unread_count > 0 ? 'text-twitter-black font-semibold' : 'text-twitter-dark-gray'
            ]"
          >
            <span v-if="chat.last_message?.sender_username === currentUsername">You: </span>
            {{ chat.last_message?.content || 'No messages yet' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import UserAvatar from './UserAvatar.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  chats: {
    type: Array,
    default: () => []
  },
  selectedChatId: {
    type: String,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['select-chat', 'new-chat'])

const authStore = useAuthStore()

const currentUsername = computed(() => authStore.user?.username)

const formatTime = (dateString) => {
  if (!dateString) return ''

  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)

  if (diffInSeconds < 60) {
    return 'now'
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
