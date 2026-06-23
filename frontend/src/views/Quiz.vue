<template>
  <div class="container">
    <div class="page-header">
      <h1>测验中心</h1>
      <p>选择题 · 拼写 · 英译中，检验你的学习成果</p>
    </div>

    <!-- 新建测验 -->
    <div class="section">
      <h3 class="section-title">开始新测验</h3>
      <div class="quiz-type-grid">
        <div class="quiz-type-card card card-interactive" @click="startQuiz('choice')">
          <div class="qt-icon" style="background:rgba(0,212,255,0.1);color:var(--accent);">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          </div>
          <h4>选择题</h4>
          <p>从四个选项中选出正确答案</p>
        </div>
        <div class="quiz-type-card card card-interactive" @click="startQuiz('spelling')">
          <div class="qt-icon" style="background:rgba(0,230,118,0.1);color:var(--success);">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>
          </div>
          <h4>拼写题</h4>
          <p>看中文写出对应的英文单词</p>
        </div>
        <div class="quiz-type-card card card-interactive" @click="startQuiz('listening')">
          <div class="qt-icon" style="background:rgba(255,171,0,0.1);color:var(--warning);">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          </div>
          <h4>英译中</h4>
          <p>看英文写出对应的中文意思</p>
        </div>
      </div>
    </div>

    <!-- 设置弹窗 -->
    <div class="modal-overlay" v-if="showSetup" @click.self="showSetup = false">
      <div class="modal card">
        <h3>{{ setupTitle }}</h3>
        <div class="form-group">
          <label>题目数量</label>
          <BaseSelect v-model="questionCount" :options="questionCountOptions" />
        </div>
        <div class="form-group">
          <label>分类（可选）</label>
          <BaseSelect v-model="quizCategory" :options="quizCategoryOptions" />
        </div>
        <div class="modal-actions">
          <button class="btn btn-ghost" @click="showSetup = false">取消</button>
          <button class="btn btn-primary" @click="goQuiz">开始答题</button>
        </div>
      </div>
    </div>

    <!-- 测验历史 -->
    <div class="section" v-if="history.length">
      <h3 class="section-title">测验历史</h3>
      <div class="quiz-list">
        <div v-for="q in history" :key="q.id" class="quiz-item card card-interactive" @click="$router.push(`/quiz/result/${q.id}`)">
          <div class="qi-left">
            <span class="badge" :class="typeBadgeClass(q.quiz_type)">{{ typeMap[q.quiz_type] || q.quiz_type }}</span>
            <span class="qi-date">{{ formatDate(q.completed_at) }}</span>
          </div>
          <div class="qi-right">
            <span class="qi-score" :style="{ color: scoreColor(q.score) }">{{ q.score }}<small>分</small></span>
            <span class="qi-detail">{{ q.correct_answers }}/{{ q.total_questions }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { quizAPI } from '@/api'
import BaseSelect from '@/components/BaseSelect.vue'

const router = useRouter()
const history = ref([])
const showSetup = ref(false)
const quizType = ref('')
const questionCount = ref(10)
const quizCategory = ref('')

const questionCountOptions = [
  { value: 5, label: '5 题' },
  { value: 10, label: '10 题' },
  { value: 20, label: '20 题' },
  { value: 30, label: '30 题' }
]

const quizCategoryOptions = [
  { value: '', label: '全部' },
  { value: 'junior', label: '初中' },
  { value: 'senior', label: '高中' },
  { value: 'cet4', label: '四级' },
  { value: 'cet6', label: '六级' },
  { value: 'postgraduate', label: '考研' },
  { value: 'toefl', label: '托福' },
  { value: 'sat', label: 'SAT' },
  { value: '', label: '──', disabled: true },
  { value: 'basic', label: '基础' },
  { value: 'intermediate', label: '中级' },
  { value: 'advanced', label: '高级' },
  { value: 'business', label: '商务' },
  { value: 'travel', label: '旅游' }
]

const typeMap = { choice: '选择题', spelling: '拼写题', listening: '英译中' }
const typeTitleMap = { choice: '选择题测验', spelling: '拼写测验', listening: '英译中测验' }
const setupTitle = computed(() => typeTitleMap[quizType.value] || '')

function typeBadgeClass(t) { return t === 'choice' ? 'badge-accent' : t === 'spelling' ? 'badge-warning' : 'badge-success' }
function formatDate(d) { return new Date(d).toLocaleDateString('zh-CN') }
function scoreColor(s) { return s >= 80 ? 'var(--success)' : s >= 60 ? 'var(--warning)' : 'var(--danger)' }

function startQuiz(type) { quizType.value = type; showSetup.value = true }
function goQuiz() {
  showSetup.value = false
  router.push({ path: `/quiz/take/${quizType.value}`, query: { count: questionCount.value, category: quizCategory.value } })
}

onMounted(async () => {
  try { const res = await quizAPI.getHistory(); history.value = res.data.results }
  catch (e) { console.error('加载历史失败', e) }
})
</script>

<style scoped>
.section { margin-top: 36px; }
.section-title { font-family: var(--font-heading); font-size: 17px; font-weight: 700; margin-bottom: 16px; color: var(--text); }
.quiz-type-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
@media (max-width: 640px) { .quiz-type-grid { grid-template-columns: 1fr; } }
.quiz-type-card { text-align: center; padding: 36px 20px; }
.qt-icon { width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 14px; }
.quiz-type-card h4 { font-family: var(--font-heading); font-size: 17px; margin-bottom: 6px; color: var(--text); }
.quiz-type-card p { font-size: 13px; color: var(--text-muted); }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 16px; }
.modal { width: 400px; max-width: 100%; padding: 32px; }
.modal h3 { font-family: var(--font-heading); font-size: 20px; margin-bottom: 22px; color: var(--text); }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 24px; }

.quiz-list { display: flex; flex-direction: column; gap: 8px; }
.quiz-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; }
.qi-left { display: flex; align-items: center; gap: 12px; }
.qi-date { font-size: 13px; color: var(--text-muted); }
.qi-right { display: flex; align-items: center; gap: 8px; }
.qi-score { font-family: var(--font-heading); font-size: 22px; font-weight: 800; }
.qi-score small { font-size: 14px; font-weight: 500; }
.qi-detail { font-size: 13px; color: var(--text-muted); }
</style>
