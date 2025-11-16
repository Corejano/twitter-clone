<template>
  <div class="flex h-screen">
    <div
      :class="[
        'border-r border-twitter-gray',
        selectedChat && 'hidden lg:block',
        'w-full lg:w-96 flex-shrink-0'
      ]"
    >
      <ChatList
        :chats="sortedChats"
        :selected-chat-id="selectedChat?.id"
        :loading="loading"
        @select-chat="handleSelectChat"
        @new-chat="showNewChatModal = true"
      />
    </div>

    <div :class="['flex-1', !selectedChat && 'hidden lg:block']">
      <ChatWindow
        :chat="selectedChat"
        :loading="chatLoading"
        @close="handleCloseChat"
      />
    </div>

    <NewChatModal
      :is-open="showNewChatModal"
      @close="showNewChatModal = false"
      @chat-created="handleChatCreated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import ChatList from '@/components/ChatList.vue'
import ChatWindow from '@/components/ChatWindow.vue'
import NewChatModal from '@/components/NewChatModal.vue'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()

const selectedChat = ref(null)
const loading = ref(false)
const chatLoading = ref(false)
const showNewChatModal = ref(false)

const sortedChats = computed(() => chatStore.sortedChats)

let refreshInterval = null

onMounted(async () => {
  await fetchChats()

  if (route.query.chatId) {
    await loadChatById(route.query.chatId)
  }

  refreshInterval = setInterval(async () => {
    await fetchChats(false)
  }, 60000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  chatStore.clearCurrentChat()
})

const fetchChats = async (showLoading = true) => {
  if (showLoading) {
    loading.value = true
  }
  try {
    await chatStore.fetchChats()
  } catch (error) {
    console.error('Failed to fetch chats:', error)
  } finally {
    if (showLoading) {
      loading.value = false
    }
  }
}

const loadChatById = async (chatId) => {
  chatLoading.value = true
  try {
    const chat = await chatStore.fetchChatById(chatId)
    selectedChat.value = chat
    chatStore.setCurrentChat(chat)
  } catch (error) {
    console.error('Failed to load chat:', error)
  } finally {
    chatLoading.value = false
  }
}

const handleSelectChat = async (chat) => {
  chatLoading.value = true

  try {
    const fullChat = await chatStore.fetchChatById(chat.id)
    selectedChat.value = fullChat
    chatStore.setCurrentChat(fullChat)

    router.push({
      query: { chatId: chat.id }
    })

    await chatStore.markChatAsRead(chat.id)
  } catch (error) {
    console.error('Failed to select chat:', error)
  } finally {
    chatLoading.value = false
  }
}

const handleCloseChat = () => {
  selectedChat.value = null
  chatStore.clearCurrentChat()

  router.push({
    query: {}
  })
}

const handleChatCreated = async (chat) => {
  await fetchChats()
  await handleSelectChat(chat)
}
</script>
