<template>
  <div class="auth-page">
    <div class="auth-wrapper">
      <div class="auth-brand">
        <div class="auth-logo">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
          </svg>
        </div>
        <h1 class="auth-name">EnglishGo</h1>
        <p class="auth-slogan">智能英语学习平台</p>
      </div>
      <div class="auth-card card">
        <h2>登录账号</h2>
        <p class="auth-subtitle">欢迎回来，继续你的学习之旅</p>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="form.username" class="form-input" placeholder="请输入用户名" autocomplete="username" required />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="form.password" type="password" class="form-input" placeholder="请输入密码" autocomplete="current-password" required />
          </div>
          <p class="error-msg" v-if="error">{{ error }}</p>
          <button type="submit" class="btn btn-primary btn-lg btn-block" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
        <p class="auth-footer">
          还没有账号？<router-link to="/register">立即注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authAPI } from '@/api'

const router = useRouter()
const auth = useAuthStore()
const form = reactive({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const res = await authAPI.login(form)
    auth.setAuth(res.data)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.error || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  padding: 24px;
}
[data-theme-style="future"] .auth-page {
  background: radial-gradient(ellipse at 50% 0%, rgba(0,212,255,0.08) 0%, transparent 60%), var(--bg);
}
.auth-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  width: 100%;
}
.auth-brand { text-align: center; }
.auth-logo {
  color: var(--accent);
  margin-bottom: 12px;
  animation: pulse-glow 2s ease-in-out infinite;
}
.auth-name {
  font-family: var(--font-heading);
  font-size: 32px;
  font-weight: 800;
  color: var(--text);
  letter-spacing: -0.03em;
}
.auth-slogan {
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 4px;
}
.auth-card {
  width: 400px;
  max-width: 100%;
  padding: 40px;
}
.auth-card h2 {
  text-align: center;
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--text);
}
.auth-subtitle {
  text-align: center;
  color: var(--text-muted);
  margin-bottom: 28px;
  font-size: 14px;
}
.error-msg {
  color: var(--danger);
  font-size: 13px;
  margin-bottom: 12px;
  text-align: center;
}
.auth-footer {
  text-align: center;
  margin-top: 22px;
  font-size: 14px;
  color: var(--text-muted);
}
</style>
