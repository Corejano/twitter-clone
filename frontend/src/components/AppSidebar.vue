<template>
  <div class="flex flex-col h-screen border-r border-twitter-gray text-black px-4 sticky top-0">
    <div class="flex flex-col space-y-2 mt-2">
      <router-link to="/home" class="flex items-center p-3 rounded-full hover:bg-twitter-light-gray transition-colors">
        <svg class="w-8 h-8 text-twitter-blue" fill="currentColor" viewBox="0 0 24 24">
          <path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"/>
        </svg>
      </router-link>

      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center space-x-4 p-3 rounded-full hover:bg-twitter-light-gray transition-colors relative"
      >
        <div class="relative">
          <component :is="item.icon" class="w-7 h-7" />
          <div
            v-if="item.badge && item.badge > 0"
            class="absolute -top-1 -right-1 bg-twitter-blue text-white text-xs font-bold rounded-full min-w-[18px] h-[18px] flex items-center justify-center px-1"
          >
            {{ item.badge > 9 ? '9+' : item.badge }}
          </div>
        </div>
        <span class="text-xl hidden xl:block">{{ item.label }}</span>
      </router-link>

      <button
        @click="handleLogout"
        class="flex items-center space-x-4 p-3 rounded-full hover:bg-twitter-light-gray transition-colors text-left"
      >
        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
        </svg>
        <span class="text-xl hidden xl:block">Logout</span>
      </button>
    </div>

    <div v-if="authStore.user" class="mt-auto mb-4 p-3 rounded-full hover:bg-twitter-light-gray transition-colors cursor-pointer" @click="goToProfile">
      <div class="flex items-center space-x-3">
        <UserAvatar
          :src="authStore.user.avatar"
          :full-name="authStore.user.full_name"
          size="md"
        />
        <div class="hidden xl:block flex-1 min-w-0">
          <p class="font-bold text-twitter-black truncate">{{ authStore.user.full_name }}</p>
          <p class="text-twitter-dark-gray text-sm truncate">@{{ authStore.user.username }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, h, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { useNotifications } from '@/composables/useNotifications'
import UserAvatar from './UserAvatar.vue'

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()
const { connect, disconnect } = useNotifications()

onMounted(() => {
  if (authStore.isAuthenticated) {
    chatStore.fetchChats()
    connect()
  }
})

const HomeIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
)

const SearchIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' })
)

const MessagesIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' })
)

const UserIcon = (props) => h('svg', { ...props, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' })
)

const menuItems = computed(() => [
  { path: '/home', label: 'Home', icon: HomeIcon },
  { path: '/search', label: 'Explore', icon: SearchIcon },
  { path: '/messages', label: 'Messages', icon: MessagesIcon, badge: chatStore.totalUnreadCount },
  { path: `/users/${authStore.user?.username}`, label: 'Profile', icon: UserIcon },
])

const goToProfile = () => {
  if (authStore.user) {
    router.push(`/users/${authStore.user.username}`)
  }
}

const handleLogout = async () => {
  disconnect()
  await authStore.logout()
  router.push('/login')
}
</script>
