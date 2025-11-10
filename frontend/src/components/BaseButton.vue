<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'font-bold rounded-full transition-colors duration-200 inline-flex items-center justify-center',
      sizeClasses,
      variantClasses,
      disabled || loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
    ]"
    @click="$emit('click', $event)"
  >
    <slot v-if="!loading" />
    <span v-else>Loading...</span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline', 'text', 'danger'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'px-4 py-1.5 text-sm',
    md: 'px-6 py-2 text-base',
    lg: 'px-8 py-3 text-lg'
  }
  return sizes[props.size]
})

const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-twitter-blue text-white hover:bg-twitter-dark-blue',
    secondary: 'bg-twitter-black text-white hover:bg-gray-800',
    outline: 'border border-twitter-gray text-twitter-black hover:bg-twitter-light-gray',
    text: 'text-twitter-blue hover:bg-blue-50',
    danger: 'bg-red-600 text-white hover:bg-red-700'
  }
  return variants[props.variant]
})
</script>
