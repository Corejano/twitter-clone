<template>
  <AppLayout v-if="$route.meta.layout === 'app'">
    <RouterView />
  </AppLayout>
  <RouterView v-else />
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/components/AppLayout.vue'

const authStore = useAuthStore()

onMounted(() => {
  authStore.initializeAuth()
})
</script>
