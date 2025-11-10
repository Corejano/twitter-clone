<template>
  <div class="flex min-h-screen bg-white mx-auto" style="max-width: 1600px;">
    <div class="w-20 xl:w-72 flex-shrink-0">
      <AppSidebar />
    </div>

    <main class="flex-1 border-r border-twitter-gray min-w-0">
      <slot />
    </main>

    <div class="hidden lg:block w-80 xl:w-96 p-4 flex-shrink-0">
      <div class="sticky top-0">
        <div class="bg-twitter-light-gray rounded-2xl p-4 mb-4">
          <h2 class="text-xl font-bold text-twitter-black mb-3">Search</h2>
          <div class="relative">
            <input
              type="text"
              v-model="searchQuery"
              @input="handleSearch"
              placeholder="Search users..."
              class="w-full px-4 py-2 bg-white rounded-full border border-twitter-gray focus:outline-none focus:border-twitter-blue"
            />
          </div>
          <div v-if="searchResults.length > 0" class="mt-3 space-y-2">
            <div
              v-for="user in searchResults"
              :key="user.username"
              @click="goToProfile(user.username)"
              class="flex items-center p-2 hover:bg-white rounded-lg cursor-pointer transition-colors"
            >
              <UserAvatar
                :src="user.avatar"
                :full-name="user.full_name"
                size="sm"
                class="mr-2"
              />
              <div class="flex-1 min-w-0">
                <p class="font-bold text-sm text-twitter-black truncate">{{ user.full_name }}</p>
                <p class="text-xs text-twitter-dark-gray truncate">@{{ user.username }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProfileStore } from '@/stores/profile'
import AppSidebar from './AppSidebar.vue'
import UserAvatar from './UserAvatar.vue'

const router = useRouter()
const profileStore = useProfileStore()

const searchQuery = ref('')
const searchResults = ref([])

let searchTimeout = null

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)

  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    try {
      const results = await profileStore.searchUsers(searchQuery.value)
      searchResults.value = results
    } catch (error) {
      console.error('Search error:', error)
    }
  }, 300)
}

const goToProfile = (username) => {
  searchQuery.value = ''
  searchResults.value = []
  router.push(`/users/${username}`)
}
</script>
