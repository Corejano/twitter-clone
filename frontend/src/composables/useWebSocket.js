import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function useWebSocket() {
  const authStore = useAuthStore()
  const ws = ref(null)
  const isConnected = ref(false)
  const isTyping = ref(false)
  const typingUser = ref(null)

  let reconnectTimeout = null
  let reconnectAttempts = 0
  const maxReconnectAttempts = 5
  const reconnectDelay = 3000

  const connect = (chatId, onMessage, onMessageRead, onError) => {
    if (!authStore.accessToken || !chatId) {
      console.error('Cannot connect: missing token or chatId')
      return
    }

    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
    const url = `${wsUrl}/ws/chat/${chatId}/?token=${authStore.accessToken}`

    try {
      ws.value = new WebSocket(url)

      ws.value.onopen = () => {
        console.log('WebSocket connected')
        isConnected.value = true
        reconnectAttempts = 0
      }

      ws.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)

          if (data.type === 'typing') {
            typingUser.value = data.username
            isTyping.value = data.is_typing
          } else if (data.type === 'chat_message') {
            if (onMessage) {
              onMessage(data.message)
            }
          } else if (data.type === 'message_read') {
            if (onMessageRead) {
              onMessageRead(data.message_id)
            }
          } else if (data.type === 'error') {
            console.error('WebSocket error:', data.message)
            if (onError) {
              onError(data.message)
            }
          }
        } catch (err) {
          console.error('Error parsing WebSocket message:', err)
        }
      }

      ws.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        if (onError) {
          onError(error)
        }
      }

      ws.value.onclose = () => {
        console.log('WebSocket disconnected')
        isConnected.value = false

        if (reconnectAttempts < maxReconnectAttempts) {
          reconnectAttempts++
          reconnectTimeout = setTimeout(() => {
            console.log(`Attempting to reconnect (${reconnectAttempts}/${maxReconnectAttempts})...`)
            connect(chatId, onMessage, onMessageRead, onError)
          }, reconnectDelay)
        }
      }
    } catch (err) {
      console.error('Error creating WebSocket:', err)
      if (onError) {
        onError(err)
      }
    }
  }

  const disconnect = () => {
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
      reconnectTimeout = null
    }

    if (ws.value) {
      ws.value.close()
      ws.value = null
    }

    isConnected.value = false
    reconnectAttempts = 0
  }

  const sendMessage = (content) => {
    if (ws.value && isConnected.value) {
      ws.value.send(JSON.stringify({
        type: 'chat_message',
        content: content
      }))
    } else {
      console.error('WebSocket is not connected')
    }
  }

  const sendTyping = (isTypingNow) => {
    if (ws.value && isConnected.value) {
      ws.value.send(JSON.stringify({
        type: 'typing',
        is_typing: isTypingNow
      }))
    }
  }

  const markAsRead = (messageId) => {
    if (ws.value && isConnected.value) {
      ws.value.send(JSON.stringify({
        type: 'mark_read',
        message_id: messageId
      }))
    }
  }

  return {
    ws,
    isConnected,
    isTyping,
    typingUser,
    connect,
    disconnect,
    sendMessage,
    sendTyping,
    markAsRead
  }
}
