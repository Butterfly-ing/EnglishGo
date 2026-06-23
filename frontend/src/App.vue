<template>
  <div id="app-root">
    <NavBar v-if="auth.isLoggedIn" />
    <main :class="{ 'with-nav': auth.isLoggedIn }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import NavBar from '@/components/NavBar.vue'

const auth = useAuthStore()
const theme = useThemeStore()

onMounted(() => {
  auth.initAuth()
})
</script>

<style scoped>
main {
  min-height: 100vh;
  padding: 24px;
  background: var(--bg);
  transition: background var(--transition);
}
main.with-nav {
  padding-top: 80px;
}
@media (max-width: 768px) {
  main { padding: 16px; }
  main.with-nav { padding-top: 72px; }
}
</style>
