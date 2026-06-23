<template>
  <div class="container">
    <div class="loading" v-if="loading"><div class="spinner"></div></div>

    <div v-else-if="word">
      <button class="btn btn-ghost btn-sm" @click="$router.back()" style="margin-bottom:20px">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        返回列表
      </button>

      <div class="detail-card card">
        <div class="detail-header">
          <div>
            <h1 class="detail-english">{{ word.english }}</h1>
            <span class="detail-phonetic" v-if="word.phonetic">{{ word.phonetic }}</span>
          </div>
          <div class="detail-actions">
            <button class="btn" :class="word.is_favorite ? 'btn-danger btn-sm' : 'btn-ghost btn-sm'" @click="toggleFavorite">
              <svg width="14" height="14" viewBox="0 0 24 24" :fill="word.is_favorite ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              {{ word.is_favorite ? '取消收藏' : '收藏' }}
            </button>
            <button class="btn" :class="word.mastered ? 'btn-success btn-sm' : 'btn-ghost btn-sm'" @click="markMastered">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              {{ word.mastered ? '已掌握' : '标记掌握' }}
            </button>
          </div>
        </div>

        <div class="detail-chinese">{{ word.chinese }}</div>

        <div class="detail-meta">
          <div class="meta-item">
            <span class="meta-label">词性</span>
            <span class="badge badge-accent">{{ posMap[word.part_of_speech] || word.part_of_speech }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">分类</span>
            <span class="badge badge-success">{{ catMap[word.category] || word.category }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">难度</span>
            <span class="badge" :class="diffBadgeClass">{{ '★'.repeat(word.difficulty || 1) }}</span>
          </div>
        </div>

        <div class="detail-example" v-if="word.example">
          <div class="example-label">例句</div>
          <p>{{ word.example }}</p>
        </div>

        <div class="detail-stats" v-if="word.practice_count > 0">
          <div class="stats-label">学习记录</div>
          <div class="stats-row">
            <div class="stat-item">
              <div class="stat-num">{{ word.practice_count }}</div>
              <div class="stat-lbl">练习次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-num">{{ word.correct_count }}</div>
              <div class="stat-lbl">正确次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-num">{{ accuracy }}%</div>
              <div class="stat-lbl">正确率</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { vocabularyAPI } from '@/api'

const route = useRoute()
const word = ref(null)
const loading = ref(true)

const posMap = { noun: '名词', verb: '动词', adjective: '形容词', adverb: '副词', preposition: '介词', conjunction: '连词', pronoun: '代词', phrase: '短语' }
const catMap = { basic: '基础', intermediate: '中级', advanced: '高级', business: '商务', travel: '旅游' }

const diffBadgeClass = computed(() => {
  const d = word.value?.difficulty || 1
  return d <= 2 ? 'badge-success' : d <= 3 ? 'badge-warning' : 'badge-danger'
})
const accuracy = computed(() => {
  if (!word.value || word.value.practice_count === 0) return 0
  return Math.round((word.value.correct_count / word.value.practice_count) * 100)
})

async function fetchWord() {
  loading.value = true
  try { const res = await vocabularyAPI.getWord(route.params.id); word.value = res.data }
  catch (e) { console.error('加载失败', e) }
  finally { loading.value = false }
}
async function toggleFavorite() {
  try { const res = await vocabularyAPI.toggleFavorite(word.value.id); word.value.is_favorite = res.data.is_favorite }
  catch (e) { console.error('操作失败', e) }
}
async function markMastered() {
  try { await vocabularyAPI.markMastered(word.value.id); word.value.mastered = true }
  catch (e) { console.error('操作失败', e) }
}
onMounted(() => fetchWord())
</script>

<style scoped>
.detail-card { padding: 36px; }
.detail-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap; }
.detail-english { font-family: var(--font-heading); font-size: 36px; font-weight: 800; color: var(--text); letter-spacing: -0.03em; }
.detail-phonetic { font-size: 18px; color: var(--text-muted); margin-left: 14px; }
.detail-actions { display: flex; gap: 8px; }
.detail-chinese { font-size: 22px; color: var(--text-secondary); margin-top: 8px; font-weight: 500; }
.detail-meta { display: flex; gap: 24px; margin-top: 22px; }
.meta-item { display: flex; align-items: center; gap: 8px; }
.meta-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.detail-example {
  margin-top: 28px; padding: 18px 20px;
  background: var(--bg-hover); border-radius: var(--radius);
  border-left: 3px solid var(--border-accent);
}
.example-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 8px; }
.detail-example p { font-size: 16px; color: var(--text-secondary); font-style: italic; }
.detail-stats { margin-top: 28px; }
.stats-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 14px; }
.stats-row { display: flex; gap: 36px; }
.stat-num { font-family: var(--font-heading); font-size: 24px; font-weight: 800; color: var(--accent); }
.stat-lbl { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
</style>
