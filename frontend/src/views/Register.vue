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
        <p class="auth-slogan">开启你的英语学习之旅</p>
      </div>
      <div class="auth-card card">
        <h2>注册账号</h2>
        <p class="auth-subtitle">加入我们，一起提升英语水平</p>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="form.username" class="form-input" placeholder="请输入用户名" autocomplete="username" required />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="form.email" type="email" class="form-input" placeholder="请输入邮箱" autocomplete="email" required />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="form.password" type="password" class="form-input" placeholder="至少6位密码" autocomplete="new-password" required />
          </div>
          <div class="form-group">
            <label>确认密码</label>
            <input v-model="form.password2" type="password" class="form-input" placeholder="再次输入密码" autocomplete="new-password" required />
          </div>
          <p class="error-msg" v-if="error">{{ error }}</p>
          <button type="submit" class="btn btn-primary btn-lg btn-block" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>
        <p class="auth-footer">
          已有账号？<router-link to="/login">立即登录</router-link>
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
const form = reactive({ username: '', email: '', password: '', password2: '' })
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  if (form.password !== form.password2) {
    error.value = '两次密码不一致'
    return
  }
  loading.value = true
  try {
    const res = await authAPI.register(form)
    auth.setAuth(res.data)
    router.push('/')
  } catch (err) {
    const data = err.response?.data
    if (data) {
      error.value = Object.values(data).flat().join('；') || '注册失败'
    } else {
      error.value = '注册失败，请稍后再试'
    }
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
  background: radial-gradient(ellipse at 50% 0%, rgba(123,97,255,0.05) 0%, transparent 60%), var(--bg);
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
.auth-subtitle { text-align: center; color: var(--text-muted); margin-bottom: 28px; font-size: 14px; }
.error-msg { color: var(--danger); font-size: 13px; margin-bottom: 12px; text-align: center; }
.auth-footer { text-align: center; margin-top: 22px; font-size: 14px; color: var(--text-muted); }
</style>
