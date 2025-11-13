<template>
  <div>
    <div class="border-b border-twitter-gray sticky top-0 bg-white bg-opacity-95 backdrop-blur z-10">
      <div class="px-4 py-3">
        <h2 class="text-xl font-bold text-twitter-black">Home</h2>
      </div>
    </div>

    <PostForm @posted="handleNewPost" />

    <div v-if="loading && posts.length === 0" class="py-20 text-center">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-twitter-blue"></div>
    </div>

    <div v-else-if="posts.length === 0" class="py-20 text-center text-twitter-dark-gray">
      <svg class="w-16 h-16 mx-auto mb-4 text-twitter-blue" fill="currentColor" viewBox="0 0 24 24">
        <path d="M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z"/>
      </svg>
      <h3 class="text-2xl font-bold text-twitter-black mb-2">No posts yet</h3>
      <p class="text-twitter-dark-gray mb-4">Follow some users to see their posts here</p>
    </div>

    <div v-else>
      <PostCard
        v-for="post in posts"
        :key="post.id"
        :post="post"
        @deleted="handlePostDeleted"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePostsStore } from '@/stores/posts'
import PostForm from '@/components/PostForm.vue'
import PostCard from '@/components/PostCard.vue'

const postsStore = usePostsStore()

const posts = ref([])
const loading = ref(false)

onMounted(async () => {
  await fetchPosts()
})

const fetchPosts = async () => {
  loading.value = true
  try {
    await postsStore.fetchPosts()
    posts.value = postsStore.posts
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  } finally {
    loading.value = false
  }
}

const handleNewPost = async () => {
  await fetchPosts()
}

const handlePostDeleted = (postId) => {
  posts.value = posts.value.filter(post => post.id !== postId)
}
</script>
