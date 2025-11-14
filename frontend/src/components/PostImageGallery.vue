<template>
  <div
    v-if="images && images.length > 0"
    :class="galleryClasses"
  >
    <div
      v-for="(image, index) in images"
      :key="image.id"
      :class="imageClasses(index)"
      @click="$emit('imageClick', index)"
    >
      <img
        :src="image.image"
        :alt="`Image ${index + 1}`"
        class="w-full rounded-2xl"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  }
})

defineEmits(['imageClick'])

const galleryClasses = computed(() => {
  const count = props.images.length

  if (count === 1) {
    return 'grid grid-cols-1 gap-0.5'
  } else if (count === 2) {
    return 'grid grid-cols-2 gap-0.5'
  } else if (count === 3) {
    return 'grid grid-cols-2 gap-0.5'
  } else {
    return 'grid grid-cols-2 gap-0.5'
  }
})

const imageClasses = (index) => {
  const count = props.images.length
  let classes = 'cursor-pointer'

  if (count === 3 && index === 0) {
    classes += ' row-span-2'
  }

  return classes
}
</script>

<style scoped>
.row-span-2 {
  grid-row: span 2;
}

img {
  display: block;
  max-height: 500px;
  object-fit: contain;
  background-color: #F7F9F9;
}
</style>
