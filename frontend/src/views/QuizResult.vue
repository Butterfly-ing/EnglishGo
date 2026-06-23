<template>
  <div class="container">
    <div class="loading" v-if="loading"><div class="spinner"></div></div>

    <div v-else-if="record">
      <!-- 总分 -->
      <div class="result-hero card">
        <div class="result-score" :style="{ color: scoreColor }">{{ record.score }}<small>分</small></div>
        <div class="result-subtitle">{{ scoreLabel }}</div>
        <div class="result-summary">
          <div class="rs-item">
            <div class="rs-num">{{ record.total_questions }}</div>
            <div class="rs-lbl">总题数</div>
          </div>
          <div class="rs-item">
            <div class="rs-num" style="color:var(--success)">{{ record.correct_answers }}</div>
            <div class="rs-lbl">正确</div>
          </div>
          <div class="rs-item">
            <div class="rs-num" style="color:var(--danger)">{{ record.total_questions - record.correct_answers }}</div>
            <div class="rs-lbl">错误</div>
          </div>
        </div>
      </div>

      <!-- 详情 -->
      <div class="section">
        <h3 class="section-title">答题详情</h3>
        <div class="detail-list">
          <div v-for="d in record.details" :key="d.id" class="detail-item card" :class="{ correct: d.is_correct, wrong: !d.is_correct }">
            <div class="di-status">
              <svg v-if="d.is_correct" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--danger)" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </div>
            <div class="di-content">
              <div class="di-question">{{ d.question }}</div>
              <div class="di-answers">
                <div v-if="!d.is_correct">
                  <span class="di-label">你的回答：</span>
                  <span class="di-wrong">{{ d.user_answer || '（未作答）' }}</span>
                </div>
                <div>
                  <span class="di-label">正确答案：</span>
                  <span class="di-correct">{{ d.correct_answer }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="result-actions">
        <button class="btn btn-ghost" @click="$router.push('/quiz')">返回测验中心</button>
        <button class="btn btn-primary" @click="retake">再来一次</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { quizAPI } from '@/api'

const route = useRoute()
const router = useRouter()
const record = ref(null)
const loading = ref(true)

const scoreColor = computed(() => {
  const s = record.value?.score || 0
  return s >= 80 ? 'var(--success)' : s >= 60 ? 'var(--warning)' : 'var(--danger)'
})
const scoreLabel = computed(() => {
  const s = record.value?.score || 0
  if (s >= 90) return '太棒了'
  if (s >= 80) return '做得很好'
  if (s >= 60) return '继续加油'
  return '需要更多练习'
})

function retake() {
  if (record.value) {
    router.push({ path: `/quiz/take/${record.value.quiz_type}`, query: { count: record.value.total_questions } })
  }
}

onMounted(async () => {
  try { const res = await quizAPI.getDetail(route.params.id); record.value = res.data }
  catch (e) { console.error('加载失败', e) }
  finally { loading.value = false }
})
</script>

<style scoped>
.result-hero { text-align: center; padding: 44px 32px; max-width: 500px; margin: 0 auto 36px; }
.result-score { font-family: var(--font-heading); font-size: 64px; font-weight: 800; line-height: 1; letter-spacing: -0.04em; }
.result-score small { font-size: 22px; font-weight: 500; margin-left: 2px; }
.result-subtitle { font-size: 16px; color: var(--text-secondary); margin-top: 8px; font-weight: 500; }
.result-summary { display: flex; justify-content: center; gap: 36px; margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--border); }
.rs-num { font-family: var(--font-heading); font-size: 26px; font-weight: 800; }
.rs-lbl { font-size: 12px; color: var(--text-muted); margin-top: 2px; text-transform: uppercase; letter-spacing: 0.04em; }

.section { margin-top: 32px; }
.section-title { font-family: var(--font-heading); font-size: 17px; font-weight: 700; margin-bottom: 14px; color: var(--text); }

.detail-list { display: flex; flex-direction: column; gap: 8px; }
.detail-item { display: flex; gap: 16px; padding: 18px; }
.detail-item.correct { border-left: 3px solid var(--success); }
.detail-item.wrong   { border-left: 3px solid var(--danger); }
.di-status { flex-shrink: 0; padding-top: 2px; }
.di-question { font-weight: 600; margin-bottom: 8px; color: var(--text); }
.di-answers { font-size: 14px; display: flex; flex-direction: column; gap: 4px; }
.di-label { color: var(--text-muted); }
.di-correct { color: var(--success); font-weight: 600; }
.di-wrong { color: var(--danger); }

.result-actions { display: flex; justify-content: center; gap: 10px; margin-top: 36px; padding-bottom: 40px; }
</style>
