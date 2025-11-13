<template>
  <div class="border-b border-twitter-gray p-4">
    <div class="flex">
      <UserAvatar
        :src="authStore.user?.avatar"
        :full-name="authStore.user?.full_name || ''"
        size="md"
        class="mr-3 flex-shrink-0"
      />
      <div class="flex-1">
        <textarea
          v-model="content"
          placeholder="What's happening?"
          class="w-full text-xl border-none text-black outline-none resize-none"
          rows="3"
          :maxlength="280"
          @input="adjustHeight"
          ref="textarea"
        />

        <div v-if="previewImages.length > 0" class="mt-3 flex flex-wrap gap-2">
          <div
            v-for="(preview, index) in previewImages"
            :key="index"
            class="relative w-24 h-24 rounded-xl overflow-hidden bg-twitter-light-gray flex-shrink-0"
          >
            <img :src="preview" :alt="`Preview ${index + 1}`" class="w-full h-full object-cover" />
            <button
              @click="removeImage(index)"
              class="absolute top-1 right-1 bg-gray-900 bg-opacity-80 text-white rounded-full p-1 hover:bg-opacity-90"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>

        <div v-if="error" class="mt-2 text-red-500 text-sm">
          {{ error }}
        </div>

        <div class="flex items-center justify-between mt-3 pt-3 border-t border-twitter-gray">
          <div class="flex items-center space-x-2">
            <label class="cursor-pointer p-2 rounded-full hover:bg-twitter-blue hover:bg-opacity-10 transition-colors">
              <input
                type="file"
                accept="image/*"
                multiple
                @change="handleFileSelect"
                class="hidden"
                :disabled="previewImages.length >= 4"
                ref="fileInput"
              />
              <svg class="w-5 h-5 text-twitter-blue" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd" />
              </svg>
            </label>
          </div>

          <div class="flex items-center space-x-3">
            <span
              :class="[
                'text-sm',
                characterCount > 280 ? 'text-red-500' : characterCount > 260 ? 'text-yellow-500' : 'text-twitter-dark-gray'
              ]"
            >
              {{ characterCount }}/280
            </span>
            <BaseButton
              variant="primary"
              size="sm"
              :disabled="!canPost"
              :loading="loading"
              @click="handleSubmit"
            >
              Post
            </BaseButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import UserAvatar from './UserAvatar.vue'
import BaseButton from './BaseButton.vue'

const emit = defineEmits(['posted'])

const authStore = useAuthStore()
const postsStore = usePostsStore()

const content = ref('')
const selectedImages = ref([])
const previewImages = ref([])
const loading = ref(false)
const error = ref(null)
const textarea = ref(null)
const fileInput = ref(null)

const characterCount = computed(() => content.value.length)

const canPost = computed(() => {
  return content.value.trim().length > 0 && content.value.length <= 280 && !loading.value
})

const adjustHeight = () => {
  if (textarea.value) {
    textarea.value.style.height = 'auto'
    textarea.value.style.height = textarea.value.scrollHeight + 'px'
  }
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  const remainingSlots = 4 - selectedImages.value.length

  if (files.length > remainingSlots) {
    error.value = `You can only upload up to 4 images. ${remainingSlots} slot(s) remaining.`
    setTimeout(() => error.value = null, 3000)
    return
  }

  const validFiles = files.filter(file => {
    if (file.size > 5 * 1024 * 1024) {
      error.value = 'Each image must be less than 5MB'
      setTimeout(() => error.value = null, 3000)
      return false
    }
    return true
  })

  validFiles.forEach(file => {
    selectedImages.value.push(file)
    const reader = new FileReader()
    reader.onload = (e) => {
      previewImages.value.push(e.target.result)
    }
    reader.readAsDataURL(file)
  })

  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const removeImage = (index) => {
  selectedImages.value.splice(index, 1)
  previewImages.value.splice(index, 1)
}

const handleSubmit = async () => {
  if (!canPost.value) return

  loading.value = true
  error.value = null

  try {
    const postData = {
      content: content.value.trim(),
      images: selectedImages.value
    }

    await postsStore.createPost(postData)

    content.value = ''
    selectedImages.value = []
    previewImages.value = []

    if (textarea.value) {
      textarea.value.style.height = 'auto'
    }

    emit('posted')
  } catch (err) {
    error.value = err.response?.data?.content?.[0] || err.response?.data?.images?.[0] || 'Failed to create post'
  } finally {
    loading.value = false
  }
}
</script>
