<template>
  <div class="flex flex-col h-full bg-white">
    <div v-if="!chat" class="flex-1 flex items-center justify-center text-center p-8">
      <div>
        <svg class="w-24 h-24 text-twitter-dark-gray mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        <h3 class="text-2xl font-bold text-twitter-black mb-2">Select a message</h3>
        <p class="text-twitter-dark-gray">Choose from your existing conversations or start a new one</p>
      </div>
    </div>

    <template v-else>
      <div class="border-b border-twitter-gray p-4 flex items-center">
        <button
          @click="$emit('close')"
          class="lg:hidden mr-3 p-2 rounded-full hover:bg-twitter-light-gray transition-colors"
        >
          <svg class="w-5 h-5 text-twitter-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <UserAvatar
          :src="chat.other_participant?.avatar"
          :full-name="chat.other_participant?.full_name"
          size="md"
          class="mr-3 cursor-pointer"
          @click="goToProfile"
        />

        <div class="flex-1 min-w-0 cursor-pointer" @click="goToProfile">
          <div class="flex items-center">
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
          </div>
          <p class="text-sm text-twitter-dark-gray truncate">@{{ chat.other_participant?.username }}</p>
        </div>
      </div>

      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4">
        <div v-if="loading" class="flex items-center justify-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-twitter-blue"></div>
        </div>

        <div v-else-if="messages.length === 0" class="flex flex-col items-center justify-center py-20 text-center">
          <svg class="w-16 h-16 text-twitter-dark-gray mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p class="text-twitter-dark-gray">No messages yet. Start the conversation!</p>
        </div>

        <div v-else>
          <MessageBubble
            v-for="message in messages"
            :key="message.id"
            :message="message"
          />
        </div>

        <div v-if="wsInstance?.isTyping.value && wsInstance?.typingUser.value" class="flex items-center mb-4">
          <p class="text-sm text-twitter-dark-gray italic">{{ wsInstance.typingUser.value }} is typing...</p>
        </div>
      </div>

      <div class="border-t border-twitter-gray p-4">
        <form @submit.prevent="handleSendMessage" class="flex items-end space-x-2">
          <textarea
            v-model="messageContent"
            @input="handleTyping"
            @keydown.enter.exact.prevent="handleSendMessage"
            placeholder="Type a message..."
            rows="1"
            class="flex-1 px-4 py-2 border border-twitter-gray rounded-full resize-none focus:outline-none focus:border-twitter-blue max-h-32 overflow-y-auto"
            style="min-height: 40px"
          />

          <button
            type="submit"
            :disabled="!messageContent.trim() || sending"
            :class="[
              'p-2 rounded-full transition-colors flex-shrink-0',
              messageContent.trim() && !sending
                ? 'bg-twitter-blue text-white hover:bg-twitter-dark-blue'
                : 'bg-twitter-light-gray text-twitter-dark-gray cursor-not-allowed'
            ]"
          >
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/>
            </svg>
          </button>
        </form>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { useWebSocket } from '@/composables/useWebSocket'
import UserAvatar from './UserAvatar.vue'
import MessageBubble from './MessageBubble.vue'

const props = defineProps({
  chat: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const messageContent = ref('')
const sending = ref(false)
const messagesContainer = ref(null)

const messages = computed(() => chatStore.messages)

const chatId = computed(() => props.chat?.id)

const wsInstance = useWebSocket()
let typingTimeout = null

onUnmounted(() => {
  wsInstance.disconnect()
})

watch(() => props.chat, (newChat, oldChat) => {
  if (newChat?.id !== oldChat?.id) {
    wsInstance.disconnect()

    if (newChat?.id) {
      setupWebSocket(newChat.id)
      scrollToBottom()
    }
  }
}, { immediate: true })

watch(() => messages.value.length, () => {
  nextTick(() => scrollToBottom())
})

const setupWebSocket = (newChatId) => {
  if (!newChatId) return

  wsInstance.connect(
    newChatId,
    async (message) => {
      chatStore.addMessage(message, authStore.user?.id)

      if (message.sender.id !== authStore.user?.id) {
        wsInstance.markAsRead(message.id)
      }
    },
    (messageId) => {
      chatStore.updateMessageReadStatus(messageId, true)
    },
    (error) => {
      console.error('WebSocket error in ChatWindow:', error)
    }
  )
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const handleSendMessage = async () => {
  const content = messageContent.value.trim()
  if (!content || sending.value || !chatId.value) return

  sending.value = true

  try {
    if (wsInstance?.isConnected.value) {
      wsInstance.sendMessage(content)
      messageContent.value = ''
      wsInstance.sendTyping(false)
    } else {
      await chatStore.sendMessage(chatId.value, content)
      messageContent.value = ''
    }
  } catch (error) {
    console.error('Failed to send message:', error)
  } finally {
    sending.value = false
  }
}

const handleTyping = () => {
  if (!wsInstance?.isConnected.value) return

  wsInstance.sendTyping(true)

  if (typingTimeout) {
    clearTimeout(typingTimeout)
  }

  typingTimeout = setTimeout(() => {
    wsInstance.sendTyping(false)
  }, 2000)
}

const goToProfile = () => {
  if (props.chat?.other_participant?.username) {
    router.push(`/users/${props.chat.other_participant.username}`)
  }
}
</script>
