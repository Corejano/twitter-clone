<template>
  <div>
    <div class="border-b border-twitter-gray sticky top-0 bg-white z-10">
      <div class="flex items-center justify-between px-4 py-3">
        <div class="flex items-center">
          <button @click="$router.back()" class="mr-8 p-2 rounded-full hover:bg-twitter-light-gray">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
          <h2 class="text-xl font-bold text-twitter-black">Edit profile</h2>
        </div>
        <BaseButton
          variant="primary"
          size="sm"
          :loading="loading"
          @click="handleSubmit"
        >
          Save
        </BaseButton>
      </div>
    </div>

    <div v-if="form.full_name !== null">
      <div class="relative">
        <div class="h-48 bg-twitter-gray relative">
          <img
            v-if="headerPreview || form.header_image"
            :src="headerPreview || form.header_image"
            alt="Header"
            class="w-full h-full object-cover"
          />
          <div class="absolute inset-0 flex items-center justify-center space-x-4">
            <label class="p-3 bg-black bg-opacity-50 rounded-full cursor-pointer hover:bg-opacity-70 transition-opacity">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <input
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleHeaderChange"
              />
            </label>
          </div>
        </div>

        <div class="px-4 -mt-16 mb-4">
          <div class="relative w-32 h-32">
            <UserAvatar
              :src="avatarPreview || form.avatar"
              :full-name="form.full_name"
              size="xl"
              class="border-4 border-white"
            />
            <label class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-full cursor-pointer hover:bg-opacity-70 transition-opacity">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <input
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleAvatarChange"
              />
            </label>
          </div>
        </div>
      </div>

      <div class="px-4 space-y-4 pb-8">
        <BaseInput
          v-model="form.full_name"
          label="Name"
          placeholder="Enter your name"
          required
          :error="errors.full_name"
        />

        <BaseTextarea
          v-model="form.bio"
          label="Bio"
          placeholder="Tell us about yourself"
          :maxlength="160"
          :show-counter="true"
          rows="3"
          :error="errors.bio"
        />

        <div v-if="errors.general" class="p-3 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ errors.general }}</p>
        </div>

        <div v-if="success" class="p-3 bg-green-50 border border-green-200 rounded-lg">
          <p class="text-sm text-green-600">Profile updated successfully!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { userService } from '@/services/users'
import UserAvatar from '@/components/UserAvatar.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseTextarea from '@/components/BaseTextarea.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  full_name: null,
  bio: '',
  avatar: null,
  header_image: null
})

const avatarFile = ref(null)
const headerFile = ref(null)
const avatarPreview = ref(null)
const headerPreview = ref(null)

const errors = reactive({
  full_name: '',
  bio: '',
  general: ''
})

const loading = ref(false)
const success = ref(false)

const handleAvatarChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      errors.general = 'Avatar must be less than 2MB'
      return
    }
    avatarFile.value = file
    avatarPreview.value = URL.createObjectURL(file)
  }
}

const handleHeaderChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      errors.general = 'Header image must be less than 5MB'
      return
    }
    headerFile.value = file
    headerPreview.value = URL.createObjectURL(file)
  }
}

const handleSubmit = async () => {
  errors.full_name = ''
  errors.bio = ''
  errors.general = ''
  success.value = false

  if (!form.full_name) {
    errors.full_name = 'Name is required'
    return
  }

  loading.value = true

  try {
    const updateData = {
      full_name: form.full_name,
      bio: form.bio
    }

    if (avatarFile.value) {
      updateData.avatar = avatarFile.value
    }

    if (headerFile.value) {
      updateData.header_image = headerFile.value
    }

    const updatedUser = await userService.updateCurrentUser(updateData)
    authStore.user = updatedUser
    success.value = true

    setTimeout(() => {
      router.push(`/users/${updatedUser.username}`)
    }, 1000)
  } catch (error) {
    if (error.response?.data) {
      const errorData = error.response.data
      Object.keys(errorData).forEach(key => {
        if (errors.hasOwnProperty(key)) {
          errors[key] = Array.isArray(errorData[key]) ? errorData[key][0] : errorData[key]
        } else {
          errors.general = 'Failed to update profile'
        }
      })
    } else {
      errors.general = 'An error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (authStore.user) {
    form.full_name = authStore.user.full_name
    form.bio = authStore.user.bio || ''
    form.avatar = authStore.user.avatar
    form.header_image = authStore.user.header_image
  }
})
</script>
