import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'

let ws = null
const isConnected = ref(false)
let reconnectTimeout = null
let reconnectAttempts = 0
let isConnecting = false
let isInitialized = false

function handleMessage(event) {
  try {
    const data = JSON.parse(event.data)

    const chatStore = useChatStore()
    const authStore = useAuthStore()

    if (data.type === 'new_message') {
      const isCurrentChat = chatStore.currentChat && data.message.chat_id === chatStore.currentChat.id
      if (!isCurrentChat) {
        chatStore.addMessage(data.message, authStore.user?.id)
      }
    } else if (data.type === 'message_read') {
      chatStore.updateMessageReadStatus(data.message_id, true)
    }
  } catch (err) {
    console.error('Error parsing notification:', err)
  }
}

function handleOpen() {
  isConnected.value = true
  isConnecting = false
  reconnectAttempts = 0
}

function handleError(error) {
  console.error('Notifications WebSocket error:', error)
  isConnecting = false
}

function handleClose(event) {
  isConnected.value = false
  isConnecting = false

  const authStore = useAuthStore()
  if (authStore.isAuthenticated) {
    reconnectAttempts++
    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000)

    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
    }

    reconnectTimeout = setTimeout(() => {
      connect()
    }, delay)
  }
}

function connect() {
  if (isConnecting) {
    return
  }

  if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
    return
  }

  const authStore = useAuthStore()
  if (!authStore.accessToken) {
    return
  }

  if (reconnectTimeout) {
    clearTimeout(reconnectTimeout)
    reconnectTimeout = null
  }

  if (ws && ws.readyState === WebSocket.CLOSING) {
    setTimeout(() => connect(), 100)
    return
  }

  isConnecting = true
  const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
  const url = `${wsUrl}/ws/notifications/?token=${authStore.accessToken}`

  try {
    ws = new WebSocket(url)
    ws.onopen = handleOpen
    ws.onmessage = handleMessage
    ws.onerror = handleError
    ws.onclose = handleClose
  } catch (err) {
    console.error('Error creating notifications WebSocket:', err)
    isConnecting = false
  }
}

function disconnect() {
  if (reconnectTimeout) {
    clearTimeout(reconnectTimeout)
    reconnectTimeout = null
  }

  if (ws) {
    ws.onclose = null
    ws.close()
    ws = null
  }

  isConnected.value = false
  isConnecting = false
  reconnectAttempts = 0
}

export function useNotifications() {
  if (!isInitialized) {
    isInitialized = true
  }

  return {
    isConnected,
    connect,
    disconnect
  }
}
