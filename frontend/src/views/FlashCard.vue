<template>
  <div class="container">
    <div class="page-header">
      <h1>闪卡学习</h1>
      <p>翻动卡片，快速记忆单词</p>
    </div>

    <!-- 设置面板 -->
    <div class="setup card" v-if="!started">
      <div class="form-group">
        <label>选择分类</label>
        <BaseSelect v-model="category" :options="flashCategoryOptions" />
      </div>
      <div class="form-group">
        <label>每轮数量</label>
        <BaseSelect v-model="count" :options="countOptions" />
      </div>
      <div class="form-group">
        <label>模式</label>
        <div class="mode-switch">
          <button :class="{ active: mode === 'en2cn' }" @click="mode = 'en2cn'">看英文 → 想中文</button>
          <button :class="{ active: mode === 'cn2en' }" @click="mode = 'cn2en'">看中文 → 想英文</button>
          <button :class="{ active: mode === 'mixed' }" @click="mode = 'mixed'">混合模式</button>
        </div>
      </div>
      <button class="btn btn-primary btn-lg btn-block" @click="startStudy" style="margin-top:20px">开始学习</button>
    </div>

    <!-- 闪卡区域 -->
    <div class="flashcard-area" v-else>
      <div class="fc-progress">
        <div class="progress-track"><div class="progress-fill" :style="{ width: progressPercent + '%' }"></div></div>
        <span class="prog-text">{{ currentIndex + 1 }} / {{ cards.length }}</span>
      </div>

      <div class="flashcard" :class="{ flipped: isFlipped }" @click="flipCard">
        <div class="card-inner">
          <div class="card-face front">
            <span class="card-tag" v-if="currentCard.category">{{ currentCard.categoryName }}</span>
            <span class="card-word">{{ currentCard.front }}</span>
            <span class="card-hint">点击翻转查看答案</span>
          </div>
          <div class="card-face back">
            <span class="card-tag" v-if="currentCard.category">{{ currentCard.categoryName }}</span>
            <span class="card-word">{{ currentCard.back }}</span>
            <span class="card-example" v-if="currentCard.example">{{ currentCard.example }}</span>
          </div>
        </div>
      </div>

      <div class="card-actions">
        <button class="btn btn-ghost" @click="prevCard" :disabled="currentIndex === 0">上一张</button>
        <button class="btn btn-danger" @click="markForgot">忘记了</button>
        <button class="btn btn-success" @click="markRemembered">记住了</button>
        <button class="btn btn-ghost" @click="nextCard" :disabled="currentIndex >= cards.length - 1">下一张</button>
      </div>

      <!-- 完成提示 -->
      <div class="complete card" v-if="completed">
        <div class="complete-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        </div>
        <h2>本轮学习完成</h2>
        <p>记住 {{ remembered }} 个，还需复习 {{ forgot }} 个</p>
        <div class="complete-actions">
          <button class="btn btn-ghost btn-sm" @click="reviewForgot" v-if="forgot > 0">复习忘记的单词</button>
          <button class="btn btn-primary btn-sm" @click="started = false">重新开始</button>
        </div>
      </div>
    </div>

    <div class="loading" v-if="loadingCards">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { vocabularyAPI, progressAPI } from '@/api'
import BaseSelect from '@/components/BaseSelect.vue'

const started = ref(false)
const category = ref('')
const count = ref(10)

const flashCategoryOptions = [
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

const countOptions = [
  { value: 10, label: '10 个' },
  { value: 20, label: '20 个' },
  { value: 30, label: '30 个' }
]
const mode = ref('en2cn')
const cards = ref([])
const currentIndex = ref(0)
const isFlipped = ref(false)
const completed = ref(false)
const remembered = ref(0)
const forgot = ref(0)
const forgotCards = ref([])
const loadingCards = ref(false)

const currentCard = computed(() => cards.value[currentIndex.value] || { front: '', back: '', category: '', categoryName: '' })
const progressPercent = computed(() => cards.value.length ? ((currentIndex.value) / cards.value.length) * 100 : 0)

const catMap = { junior:'初中', senior:'高中', cet4:'四级', cet6:'六级', postgraduate:'考研', toefl:'托福', sat:'SAT', basic:'基础', intermediate:'中级', advanced:'高级', business:'商务', travel:'旅游' }

function flipCard() { isFlipped.value = !isFlipped.value }

async function startStudy() {
  loadingCards.value = true
  try {
    const params = { page_size: count.value }
    if (category.value) params.category = category.value
    const res = await vocabularyAPI.getWords(params)
    cards.value = res.data.results.map(w => {
      let front, back
      if (mode.value === 'en2cn') { front = w.english; back = w.chinese }
      else if (mode.value === 'cn2en') { front = w.chinese; back = w.english }
      else { front = Math.random() > 0.5 ? w.english : w.chinese; back = front === w.english ? w.chinese : w.english }
      return { id: w.id, front, back, example: w.example, category: w.category, categoryName: catMap[w.category] || w.category }
    })
    currentIndex.value = 0; isFlipped.value = false; completed.value = false
    remembered.value = 0; forgot.value = 0; forgotCards.value = []
    started.value = true; loadingCards.value = false
  } catch (e) {
    console.error('加载单词失败', e); loadingCards.value = false
  }
}

function markRemembered() { remembered.value++; goNext() }
function markForgot() { forgot.value++; forgotCards.value.push(cards.value[currentIndex.value]); goNext() }

function goNext() {
  if (currentIndex.value < cards.value.length - 1) { currentIndex.value++; isFlipped.value = false }
  else {
    completed.value = true
    progressAPI.recordActivity({ words_learned: remembered.value, words_reviewed: remembered.value + forgot.value, study_minutes: Math.ceil(cards.value.length / 2) }).catch(() => {})
  }
}

function prevCard() { if (currentIndex.value > 0) { currentIndex.value--; isFlipped.value = false } }
function nextCard() { if (currentIndex.value < cards.value.length - 1) { currentIndex.value++; isFlipped.value = false } }

function reviewForgot() {
  cards.value = [...forgotCards.value]; currentIndex.value = 0; isFlipped.value = false
  completed.value = false; remembered.value = 0; forgot.value = 0; forgotCards.value = []
}
</script>

<style scoped>
.setup { max-width: 480px; margin: 0 auto; padding: 32px; }
.mode-switch { display: flex; gap: 8px; flex-wrap: wrap; }
.mode-switch button {
  flex: 1; padding: 10px 12px; border-radius: var(--radius-sm);
  background: var(--bg-hover); color: var(--text-secondary);
  font-size: 13px; font-weight: 500; min-width: 100px; transition: all var(--transition);
}
.mode-switch button.active { background: var(--accent); color: #fff; }

.flashcard-area { max-width: 600px; margin: 0 auto; }
.fc-progress { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
.progress-track { flex: 1; height: 6px; background: var(--bg-hover); border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: var(--accent); border-radius: 3px; transition: width 0.3s ease; }
.prog-text { font-size: 13px; color: var(--text-muted); white-space: nowrap; }

.flashcard { width: 100%; height: 280px; perspective: 1000px; cursor: pointer; margin-bottom: 24px; }
.card-inner { width: 100%; height: 100%; position: relative; transition: transform 0.6s cubic-bezier(0.4,0,0.2,1); transform-style: preserve-3d; }
.flashcard.flipped .card-inner { transform: rotateY(180deg); }
.card-face {
  position: absolute; width: 100%; height: 100%;
  backface-visibility: hidden; border-radius: var(--radius-lg);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 16px; box-shadow: var(--shadow-lg); padding: 24px;
}
.front { background: linear-gradient(135deg, var(--accent), var(--accent-2)); color: #fff; }
.back  { background: linear-gradient(135deg, var(--success), #059669); color: #fff; transform: rotateY(180deg); }
.card-word { font-family: var(--font-heading); font-size: 32px; font-weight: 800; text-align: center; }
.card-tag {
  position: absolute; top: 16px; left: 20px;
  font-size: 12px; font-weight: 600;
  background: rgba(255,255,255,0.25); color: #fff;
  padding: 3px 10px; border-radius: 12px;
  letter-spacing: 0.02em;
}
.card-hint { font-size: 13px; opacity: 0.7; }
.card-example { font-size: 14px; opacity: 0.75; font-style: italic; text-align: center; }

.card-actions { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 28px; }

.complete { text-align: center; padding: 40px; }
.complete-icon { margin-bottom: 12px; }
.complete h2 { font-family: var(--font-heading); font-size: 22px; margin-bottom: 6px; color: var(--text); }
.complete p { color: var(--text-secondary); margin-bottom: 20px; }
.complete-actions { display: flex; gap: 10px; justify-content: center; }
</style>
