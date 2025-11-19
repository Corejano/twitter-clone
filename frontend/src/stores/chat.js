import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { chatService } from '@/services/chat'

export const useChatStore = defineStore('chat', () => {
  const chats = ref([])
  const currentChat = ref(null)
  const messages = ref([])
  const loading = ref(false)
  const error = ref(null)

  const sortedChats = computed(() => {
    return [...chats.value].sort((a, b) => {
      const aTime = a.last_message?.created_at || a.updated_at
      const bTime = b.last_message?.created_at || b.updated_at
      return new Date(bTime) - new Date(aTime)
    })
  })

  const totalUnreadCount = computed(() => {
    return chats.value.reduce((sum, chat) => sum + (chat.unread_count || 0), 0)
  })

  async function fetchChats() {
    try {
      loading.value = true
      error.value = null
      const data = await chatService.getChats()
      chats.value = data.results || data
      return data
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch chats'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchChatById(chatId) {
    try {
      loading.value = true
      error.value = null
      const data = await chatService.getChatById(chatId)
      currentChat.value = data
      messages.value = data.messages || []
      return data
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch chat'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createChat(participantId) {
    try {
      error.value = null
      const data = await chatService.createChat(participantId)

      const existingChatIndex = chats.value.findIndex(c => c.id === data.id)
      if (existingChatIndex === -1) {
        chats.value.unshift(data)
      } else {
        chats.value[existingChatIndex] = data
      }

      return data
    } catch (err) {
      error.value = err.response?.data || 'Failed to create chat'
      throw err
    }
  }

  async function sendMessage(chatId, content) {
    try {
      error.value = null
      const message = await chatService.sendMessage(chatId, content)
      return message
    } catch (err) {
      error.value = err.response?.data || 'Failed to send message'
      throw err
    }
  }

  async function markChatAsRead(chatId) {
    try {
      await chatService.markChatAsRead(chatId)

      const chatIndex = chats.value.findIndex(c => c.id === chatId)
      if (chatIndex !== -1) {
        chats.value[chatIndex].unread_count = 0
      }

      messages.value.forEach(msg => {
        if (!msg.is_read) {
          msg.is_read = true
        }
      })
    } catch (err) {
      console.error('Failed to mark chat as read:', err)
    }
  }

  function addMessage(message, currentUserId) {
    const isCurrentChat = currentChat.value && message.chat_id === currentChat.value.id

    if (isCurrentChat) {
      const existingIndex = messages.value.findIndex(m => m.id === message.id)
      if (existingIndex === -1) {
        messages.value.push(message)
      } else {
        messages.value[existingIndex] = message
      }
    }

    const chatIndex = chats.value.findIndex(c => c.id === message.chat_id)
    if (chatIndex !== -1) {
      const chat = chats.value[chatIndex]
      const isNewMessage = !chat.last_message || chat.last_message.id !== message.id

      if (!isNewMessage) {
        return
      }

      chats.value[chatIndex].last_message = {
        id: message.id,
        content: message.content,
        sender_id: message.sender.id,
        sender_username: message.sender.username,
        created_at: message.created_at,
        is_read: message.is_read
      }
      chats.value[chatIndex].updated_at = message.created_at

      if (message.sender.id !== currentUserId && !isCurrentChat) {
        const oldUnreadCount = chat.unread_count || 0
        chats.value[chatIndex].unread_count = oldUnreadCount + 1
      }
    }
  }

  function updateMessageReadStatus(messageId, isRead) {
    const messageIndex = messages.value.findIndex(m => m.id === messageId)
    if (messageIndex !== -1) {
      messages.value[messageIndex].is_read = isRead
    }

    chats.value.forEach(chat => {
      if (chat.last_message && chat.last_message.id === messageId) {
        chat.last_message.is_read = isRead
      }
    })
  }

  function setCurrentChat(chat) {
    currentChat.value = chat
    messages.value = chat?.messages || []
  }

  function clearCurrentChat() {
    currentChat.value = null
    messages.value = []
  }

  function clearError() {
    error.value = null
  }

  return {
    chats,
    currentChat,
    messages,
    loading,
    error,
    sortedChats,
    totalUnreadCount,
    fetchChats,
    fetchChatById,
    createChat,
    sendMessage,
    markChatAsRead,
    addMessage,
    updateMessageReadStatus,
    setCurrentChat,
    clearCurrentChat,
    clearError
  }
})
