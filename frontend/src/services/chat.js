import api from './api'

export const chatService = {
  async getChats() {
    const response = await api.get('/chats/')
    return response.data
  },

  async getChatById(chatId) {
    const response = await api.get(`/chats/${chatId}/`)
    return response.data
  },

  async createChat(participantId) {
    const response = await api.post('/chats/', {
      participant_id: participantId
    })
    return response.data
  },

  async getChatMessages(chatId) {
    const response = await api.get(`/chats/${chatId}/messages/`)
    return response.data
  },

  async sendMessage(chatId, content) {
    const response = await api.post(`/chats/${chatId}/send_message/`, {
      content
    })
    return response.data
  },

  async markChatAsRead(chatId) {
    const response = await api.patch(`/chats/${chatId}/mark-read/`)
    return response.data
  }
}
