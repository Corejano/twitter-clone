<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    @click.self="closeModal"
  >
    <div class="bg-white rounded-2xl w-full max-w-xl mx-4 max-h-[80vh] flex flex-col">
      <div class="flex items-center justify-between p-4 border-b border-twitter-gray">
        <h2 class="text-xl font-bold text-twitter-black">New Message</h2>
        <button
          @click="closeModal"
          class="p-2 rounded-full hover:bg-twitter-light-gray transition-colors"
        >
          <svg class="w-5 h-5 text-twitter-black" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div class="p-4">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Search users..."
          class="w-full px-4 py-2 border border-twitter-gray rounded-full focus:outline-none focus:border-twitter-blue"
        />
      </div>

      <div class="flex-1 overflow-y-auto">
        <div v-if="searching" class="flex items-center justify-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-twitter-blue"></div>
        </div>

        <div v-else-if="searchQuery && searchResults.length === 0" class="py-8 text-center">
          <p class="text-twitter-dark-gray">No users found</p>
        </div>

        <div v-else-if="searchResults.length > 0">
          <div
            v-for="user in searchResults"
            :key="user.id"
            @click="selectUser(user)"
            class="flex items-center p-4 hover:bg-twitter-light-gray transition-colors cursor-pointer"
          >
            <UserAvatar
              :src="user.avatar"
              :full-name="user.full_name"
              size="md"
              class="mr-3"
            />
            <div class="flex-1 min-w-0">
              <div class="flex items-center">
                <span class="font-bold text-twitter-black truncate">{{ user.full_name }}</span>
                <svg
                  v-if="user.is_verified"
                  class="w-4 h-4 text-twitter-blue ml-1 flex-shrink-0"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zm-1.5 14.5l-4-4 1.414-1.414L8.5 11.672l5.086-5.086L15 8l-6.5 6.5z"/>
                </svg>
              </div>
              <p class="text-sm text-twitter-dark-gray truncate">@{{ user.username }}</p>
              <p v-if="user.bio" class="text-sm text-twitter-dark-gray truncate mt-1">{{ user.bio }}</p>
            </div>
          </div>
        </div>

        <div v-else class="py-8 text-center text-twitter-dark-gray">
          <p>Search for a user to start a conversation</p>
        </div>
      </div>

      <div v-if="error" class="px-4 py-2 bg-red-50 border-t border-red-100">
        <p class="text-sm text-red-600">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { useChatStore } from '@/stores/chat'
import UserAvatar from './UserAvatar.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'chat-created'])

const profileStore = useProfileStore()
const chatStore = useChatStore()

const searchQuery = ref('')
const searchResults = ref([])
const searching = ref(false)
const error = ref(null)

let searchTimeout = null

watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    searchQuery.value = ''
    searchResults.value = []
    error.value = null
  }
})

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)

  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    try {
      searching.value = true
      error.value = null
      const results = await profileStore.searchUsers(searchQuery.value)
      searchResults.value = results
    } catch (err) {
      console.error('Search error:', err)
      error.value = 'Failed to search users'
    } finally {
      searching.value = false
    }
  }, 300)
}

const selectUser = async (user) => {
  try {
    error.value = null
    const chat = await chatStore.createChat(user.id)
    emit('chat-created', chat)
    closeModal()
  } catch (err) {
    console.error('Failed to create chat:', err)
    error.value = err.response?.data?.error || 'Failed to create chat'
  }
}

const closeModal = () => {
  emit('close')
}
</script>
