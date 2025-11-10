<template>
  <div>
    <div class="border-b border-twitter-gray sticky top-0 bg-white z-10">
      <div class="px-4 py-3">
        <h2 class="text-xl font-bold text-twitter-black mb-3">Explore</h2>
        <div class="relative">
          <input
            type="text"
            v-model="searchQuery"
            @input="handleSearch"
            placeholder="Search users..."
            class="w-full px-4 py-3 bg-twitter-light-gray rounded-full focus:outline-none focus:bg-white focus:border focus:border-twitter-blue"
          />
          <svg class="w-5 h-5 text-twitter-dark-gray absolute left-4 top-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="text-twitter-dark-gray">Searching...</div>
    </div>

    <div v-else-if="!searchQuery" class="py-12 text-center text-twitter-dark-gray">
      <svg class="w-16 h-16 mx-auto mb-4 text-twitter-dark-gray" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      <p class="text-lg">Search for users</p>
      <p class="text-sm mt-2">Find people by their name or username</p>
    </div>

    <div v-else-if="searchResults.length === 0" class="py-12 text-center text-twitter-dark-gray">
      <p>No results found for "{{ searchQuery }}"</p>
    </div>

    <div v-else>
      <UserCard
        v-for="user in searchResults"
        :key="user.username"
        :user="user"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProfileStore } from '@/stores/profile'
import UserCard from '@/components/UserCard.vue'

const profileStore = useProfileStore()

const searchQuery = ref('')
const loading = ref(false)
const searchResults = computed(() => profileStore.searchResults)

let searchTimeout = null

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)

  if (!searchQuery.value.trim()) {
    profileStore.clearSearch()
    return
  }

  loading.value = true

  searchTimeout = setTimeout(async () => {
    try {
      await profileStore.searchUsers(searchQuery.value)
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      loading.value = false
    }
  }, 300)
}
</script>
