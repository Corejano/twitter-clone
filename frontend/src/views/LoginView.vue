<template>
  <div class="min-h-screen flex items-center justify-center bg-white">
    <div class="max-w-md w-full px-6">
      <div class="text-center mb-8">
        <svg class="w-12 h-12 text-twitter-blue mx-auto mb-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"/>
        </svg>
        <h1 class="text-3xl font-bold text-twitter-black">Sign in to Twitter</h1>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <BaseInput
          v-model="form.login"
          label="Username or Email"
          placeholder="Enter your username or email"
          required
          :error="errors.login"
        />

        <BaseInput
          v-model="form.password"
          type="password"
          label="Password"
          placeholder="Enter your password"
          required
          :error="errors.password"
        />

        <div v-if="errors.general" class="p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ errors.general }}</p>
        </div>

        <BaseButton
          type="submit"
          variant="primary"
          size="lg"
          :loading="loading"
          class="w-full"
        >
          Sign in
        </BaseButton>
      </form>

      <div class="mt-6 text-center">
        <p class="text-twitter-dark-gray">
          Don't have an account?
          <router-link to="/register" class="text-twitter-blue hover:underline">
            Sign up
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  login: '',
  password: ''
})

const errors = reactive({
  login: '',
  password: '',
  general: ''
})

const loading = ref(false)

const handleSubmit = async () => {
  errors.login = ''
  errors.password = ''
  errors.general = ''

  if (!form.login) {
    errors.login = 'Username or email is required'
    return
  }

  if (!form.password) {
    errors.password = 'Password is required'
    return
  }

  loading.value = true

  try {
    await authStore.login({
      username: form.login,
      password: form.password
    })
    router.push('/home')
  } catch (error) {
    if (error.response?.data) {
      const errorData = error.response.data
      if (errorData.detail) {
        errors.general = errorData.detail
      } else if (errorData.non_field_errors) {
        errors.general = errorData.non_field_errors[0]
      } else {
        errors.general = 'Invalid credentials. Please try again.'
      }
    } else {
      errors.general = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>
