<template>
  <div>
    <div class="border-b border-twitter-gray sticky top-0 bg-white bg-opacity-95 backdrop-blur z-10">
      <div class="flex items-center px-4 py-3">
        <button @click="$router.back()" class="mr-8 p-2 rounded-full hover:bg-twitter-light-gray">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
        </button>
        <div>
          <h2 class="text-xl font-bold text-twitter-black">{{ username }}</h2>
        </div>
      </div>
    </div>

    <div class="border-b border-twitter-gray">
      <div class="flex">
        <router-link
          :to="`/users/${username}/followers`"
          class="flex-1 py-4 text-center font-semibold text-twitter-dark-gray hover:bg-twitter-light-gray"
        >
          Followers
        </router-link>
        <router-link
          :to="`/users/${username}/following`"
          class="flex-1 py-4 text-center font-semibold text-twitter-black border-b-4 border-twitter-blue"
        >
          Following
        </router-link>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="text-twitter-dark-gray">Loading...</div>
    </div>

    <div v-else-if="following.length === 0" class="py-12 text-center text-twitter-dark-gray">
      <p>Not following anyone yet</p>
    </div>

    <div v-else>
      <UserCard
        v-for="user in following"
        :key="user.username"
        :user="user"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useProfileStore } from '@/stores/profile'
import UserCard from '@/components/UserCard.vue'

const route = useRoute()
const profileStore = useProfileStore()

const loading = ref(false)
const username = computed(() => route.params.username)
const following = computed(() => profileStore.following)

onMounted(async () => {
  loading.value = true
  try {
    await profileStore.fetchFollowing(username.value)
  } catch (error) {
    console.error('Failed to load following:', error)
  } finally {
    loading.value = false
  }
})
</script>
