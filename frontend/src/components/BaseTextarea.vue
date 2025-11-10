<template>
  <div class="w-full">
    <label v-if="label" :for="id" class="block text-sm font-medium text-twitter-dark-gray mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <div class="relative">
      <textarea
        :id="id"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :maxlength="maxlength"
        :rows="rows"
        :class="[
          'w-full px-4 py-3 border rounded-lg text-twitter-black placeholder-twitter-dark-gray transition-colors resize-none',
          error ? 'border-red-500 focus:border-red-500' : 'border-twitter-gray focus:border-twitter-blue',
          disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white',
          'focus:outline-none focus:ring-2 focus:ring-twitter-blue focus:ring-opacity-20'
        ]"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur')"
        @focus="$emit('focus')"
      />
      <span v-if="maxlength && showCounter" class="absolute right-3 bottom-3 text-sm text-twitter-dark-gray">
        {{ modelValue?.length || 0 }}/{{ maxlength }}
      </span>
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-500">{{ error }}</p>
    <p v-else-if="hint" class="mt-1 text-sm text-twitter-dark-gray">{{ hint }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  id: {
    type: String,
    default: () => `textarea-${Math.random().toString(36).substr(2, 9)}`
  },
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  maxlength: {
    type: Number,
    default: null
  },
  showCounter: {
    type: Boolean,
    default: false
  },
  rows: {
    type: Number,
    default: 4
  }
})

defineEmits(['update:modelValue', 'blur', 'focus'])
</script>
