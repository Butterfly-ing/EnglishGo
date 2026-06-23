<template>
  <div class="container">
    <div class="page-header">
      <h1>学习进度</h1>
      <p>追踪你的学习轨迹与成长曲线</p>
    </div>

    <div class="loading" v-if="loading"><div class="spinner"></div></div>

    <template v-else-if="stats">
      <!-- 统计 -->
      <div class="stats-row">
        <StatCard :value="stats.streak_days + ' 天'" label="连续打卡" bgColor="#ff5252">
          <template #icon><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></template>
        </StatCard>
        <StatCard :value="stats.learned_words" label="已学单词" bgColor="#00d4ff">
          <template #icon><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></template>
        </StatCard>
        <StatCard :value="stats.mastered_words" label="已掌握" bgColor="#00e676">
          <template #icon><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="20 6 9 17 4 12"/></svg></template>
        </StatCard>
        <StatCard :value="stats.total_study_minutes + ' 分钟'" label="学习时长" bgColor="#ffab00">
          <template #icon><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></template>
        </StatCard>
      </div>
      <div class="stats-row-2">
        <StatCard :value="stats.total_quizzes" label="完成测验" bgColor="#7b61ff">
          <template #icon><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></template>
        </StatCard>
        <StatCard :value="stats.average_score + '%'" label="平均正确率" bgColor="#9b59b6">
          <template #icon><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></template>
        </StatCard>
      </div>

      <!-- 每日图表 -->
      <div class="section">
        <h3 class="section-title">每日学习记录</h3>
        <div class="daily-chart card" v-if="dailyData.length">
          <div class="chart-bars">
            <div class="chart-bar-item" v-for="d in dailyData" :key="d.date">
              <div class="bar-stack">
                <div class="bar-learned" :style="{ height: barHeight(d.words_learned) }" :title="'新学: ' + d.words_learned"></div>
                <div class="bar-reviewed" :style="{ height: barHeight(d.words_reviewed) }" :title="'复习: ' + d.words_reviewed"></div>
              </div>
              <div class="bar-label">{{ formatShortDate(d.date) }}</div>
              <div class="bar-check" v-if="d.checked_in">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="var(--warning)" stroke="var(--warning)" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
            </div>
          </div>
          <div class="chart-legend">
            <span><span class="legend-dot" style="background:var(--accent)"></span> 新学</span>
            <span><span class="legend-dot" style="background:var(--accent-2)"></span> 复习</span>
          </div>
        </div>
        <div class="empty-state" v-else>
          <p>暂无学习记录，快去学习吧</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { progressAPI } from '@/api'
import StatCard from '@/components/StatCard.vue'

const stats = ref(null)
const dailyData = ref([])
const loading = ref(true)

function formatShortDate(d) { const parts = d.split('-'); return `${parts[1]}/${parts[2]}` }
function barHeight(count) {
  const max = Math.max(...dailyData.value.map(d => Math.max(d.words_learned, d.words_reviewed)), 1)
  return Math.max((count / max) * 120, 2) + 'px'
}

onMounted(async () => {
  try {
    const [statsRes, dailyRes] = await Promise.all([progressAPI.getStats(), progressAPI.getDaily(14)])
    stats.value = statsRes.data; dailyData.value = dailyRes.data.results
  } catch (e) { console.error('加载进度失败', e) }
  finally { loading.value = false }
})
</script>

<style scoped>
.stats-row   { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 14px; }
.stats-row-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
@media (max-width: 1024px) { .stats-row { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px)  { .stats-row, .stats-row-2 { grid-template-columns: 1fr; } }

.section { margin-top: 36px; }
.section-title { font-family: var(--font-heading); font-size: 17px; font-weight: 700; margin-bottom: 16px; color: var(--text); }

.daily-chart { padding: 28px 24px 16px; }
.chart-bars { display: flex; gap: 4px; align-items: flex-end; height: 160px; }
.chart-bar-item { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 0; }
.bar-stack { width: 100%; max-width: 28px; display: flex; flex-direction: column; justify-content: flex-end; gap: 2px; height: 130px; }
.bar-learned { background: var(--accent); border-radius: 3px 3px 0 0; min-height: 2px; transition: height 0.4s ease; }
.bar-reviewed { background: var(--accent-2); border-radius: 3px 3px 0 0; min-height: 2px; transition: height 0.4s ease; }
.bar-label { font-size: 10px; color: var(--text-muted); }
.bar-check { height: 10px; }
.chart-legend { display: flex; gap: 24px; margin-top: 12px; justify-content: center; font-size: 13px; color: var(--text-muted); }
.legend-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
</style>
