<template>
  <div class="min-h-screen flex items-center justify-center bg-white py-12">
    <div class="max-w-md w-full px-6">
      <div class="text-center mb-8">
        <svg class="w-12 h-12 text-twitter-blue mx-auto mb-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"/>
        </svg>
        <h1 class="text-3xl font-bold text-twitter-black">Join Twitter today</h1>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <BaseInput
          v-model="form.full_name"
          label="Full Name"
          placeholder="Enter your full name"
          required
          :error="errors.full_name"
        />

        <BaseInput
          v-model="form.username"
          label="Username"
          placeholder="Choose a username"
          required
          :error="errors.username"
          hint="3-15 characters, letters, numbers and underscores only"
        />

        <BaseInput
          v-model="form.email"
          type="email"
          label="Email"
          placeholder="Enter your email"
          required
          :error="errors.email"
        />

        <BaseInput
          v-model="form.password"
          type="password"
          label="Password"
          placeholder="Create a password"
          required
          :error="errors.password"
          hint="Minimum 8 characters"
        />

        <BaseInput
          v-model="form.password_confirm"
          type="password"
          label="Confirm Password"
          placeholder="Confirm your password"
          required
          :error="errors.password_confirm"
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
          Sign up
        </BaseButton>
      </form>

      <div class="mt-6 text-center">
        <p class="text-twitter-dark-gray">
          Already have an account?
          <router-link to="/login" class="text-twitter-blue hover:underline">
            Sign in
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
  full_name: '',
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const errors = reactive({
  full_name: '',
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  general: ''
})

const loading = ref(false)

const validateForm = () => {
  let isValid = true

  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.full_name) {
    errors.full_name = 'Full name is required'
    isValid = false
  }

  if (!form.username) {
    errors.username = 'Username is required'
    isValid = false
  } else if (!/^[a-zA-Z0-9_]{3,15}$/.test(form.username)) {
    errors.username = 'Username must be 3-15 characters and contain only letters, numbers, and underscores'
    isValid = false
  }

  if (!form.email) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Invalid email format'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
    isValid = false
  }

  if (!form.password_confirm) {
    errors.password_confirm = 'Please confirm your password'
    isValid = false
  } else if (form.password !== form.password_confirm) {
    errors.password_confirm = 'Passwords do not match'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  loading.value = true

  try {
    await authStore.register({
      full_name: form.full_name,
      username: form.username,
      email: form.email,
      password: form.password,
      password_confirm: form.password_confirm
    })
    router.push('/home')
  } catch (error) {
    if (error.response?.data) {
      const errorData = error.response.data
      Object.keys(errorData).forEach(key => {
        if (errors.hasOwnProperty(key)) {
          errors[key] = Array.isArray(errorData[key]) ? errorData[key][0] : errorData[key]
        } else {
          errors.general = Array.isArray(errorData[key]) ? errorData[key][0] : errorData[key]
        }
      })
    } else {
      errors.general = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>
