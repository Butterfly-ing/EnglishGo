<template>
  <div class="container">
    <div class="page-header">
      <h1>欢迎回来，{{ auth.user?.username }}</h1>
      <p>继续你的英语学习之旅</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-row" v-if="stats">
      <StatCard :value="stats.total_words"   label="词汇总量" bgColor="#00d4ff">
        <template #icon><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></template>
      </StatCard>
      <StatCard :value="stats.mastered_words" label="已掌握"   bgColor="#00e676">
        <template #icon><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="20 6 9 17 4 12"/></svg></template>
      </StatCard>
      <StatCard :value="stats.total_quizzes"  label="完成测验" bgColor="#ffab00">
        <template #icon><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></template>
      </StatCard>
      <StatCard :value="stats.streak_days + ' 天'" label="连续打卡" bgColor="#ff5252">
        <template #icon><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></template>
      </StatCard>
    </div>

    <!-- 快捷操作 -->
    <div class="section">
      <h3 class="section-title">快捷操作</h3>
      <div class="quick-grid">
        <router-link to="/study/flashcard" class="quick-card card">
          <div class="qc-icon" style="background:rgba(0,212,255,0.1);color:#00d4ff;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="2 10 22 10"/></svg>
          </div>
          <div class="qc-text">
            <div class="qc-title">闪卡学习</div>
            <div class="qc-desc">翻转卡片，快速记忆单词</div>
          </div>
        </router-link>
        <router-link to="/quiz" class="quick-card card">
          <div class="qc-icon" style="background:rgba(0,230,118,0.1);color:#00e676;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          </div>
          <div class="qc-text">
            <div class="qc-title">开始测验</div>
            <div class="qc-desc">选择题 · 拼写 · 英译中</div>
          </div>
        </router-link>
        <button class="quick-card card" @click="handleCheckin">
          <div class="qc-icon" style="background:rgba(255,171,0,0.1);color:#ffab00;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          </div>
          <div class="qc-text">
            <div class="qc-title">今日打卡</div>
            <div class="qc-desc">{{ checkinMsg || '记录今天的学习成果' }}</div>
          </div>
        </button>
      </div>
    </div>

    <!-- 最近测验 -->
    <div class="section" v-if="recentQuizzes.length">
      <h3 class="section-title">最近测验</h3>
      <div class="quiz-list">
        <div v-for="q in recentQuizzes" :key="q.id" class="quiz-item card card-interactive" @click="$router.push(`/quiz/result/${q.id}`)">
          <div class="qi-left">
            <span class="badge" :class="q.quiz_type === 'choice' ? 'badge-accent' : q.quiz_type === 'spelling' ? 'badge-warning' : 'badge-success'">
              {{ typeMap[q.quiz_type] || q.quiz_type }}
            </span>
            <span class="qi-date">{{ formatDate(q.completed_at) }}</span>
          </div>
          <div class="qi-right">
            <span class="qi-score" :style="{ color: scoreColor(q.score) }">{{ q.score }}<small>分</small></span>
            <span class="qi-detail">{{ q.correct_answers }}/{{ q.total_questions }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { progressAPI, quizAPI } from '@/api'
import StatCard from '@/components/StatCard.vue'

const auth = useAuthStore()
const stats = ref(null)
const recentQuizzes = ref([])
const checkinMsg = ref('')
const loading = ref(true)

const typeMap = { choice: '选择题', spelling: '拼写题', listening: '英译中' }

function formatDate(d) { return new Date(d).toLocaleDateString('zh-CN') }
function scoreColor(s) { return s >= 80 ? 'var(--success)' : s >= 60 ? 'var(--warning)' : 'var(--danger)' }

async function handleCheckin() {
  try {
    const res = await progressAPI.checkin()
    checkinMsg.value = `已打卡！连续 ${res.data.streak_days} 天`
    if (stats.value) stats.value.streak_days = res.data.streak_days
  } catch {
    checkinMsg.value = '打卡失败'
  }
}

onMounted(async () => {
  try {
    const [statsRes, quizRes] = await Promise.all([progressAPI.getStats(), quizAPI.getHistory()])
    stats.value = statsRes.data
    recentQuizzes.value = quizRes.data.results.slice(0, 5)
  } catch (e) {
    console.error('加载首页数据失败', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 36px;
}
@media (max-width: 1024px) { .stats-row { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px)  { .stats-row { grid-template-columns: 1fr; } }

.section { margin-top: 36px; }
.section-title {
  font-family: var(--font-heading);
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--text);
  letter-spacing: -0.01em;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
@media (max-width: 640px) { .quick-grid { grid-template-columns: 1fr; } }

.quick-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  text-align: left;
  text-decoration: none;
  color: inherit;
  background: var(--bg-card);
  border: 1px solid var(--border);
  width: 100%;
}
.qc-icon {
  width: 46px; height: 46px;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.qc-title { font-weight: 700; font-size: 15px; color: var(--text); }
.qc-desc { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

.quiz-list { display: flex; flex-direction: column; gap: 8px; }
.quiz-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; }
.qi-left { display: flex; align-items: center; gap: 12px; }
.qi-date { font-size: 13px; color: var(--text-muted); }
.qi-right { display: flex; align-items: center; gap: 8px; }
.qi-score { font-family: var(--font-heading); font-size: 22px; font-weight: 800; letter-spacing: -0.02em; }
.qi-score small { font-size: 14px; font-weight: 500; }
.qi-detail { font-size: 13px; color: var(--text-muted); }
</style>
