<template>
  <div class="container">
    <div class="page-header">
      <h1>词汇库</h1>
      <p>浏览和学习英文单词</p>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filters card">
      <div class="search-wrap">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="search" class="search-input" placeholder="搜索单词（英文/中文）..." @input="debouncedSearch" />
      </div>
      <BaseSelect v-model="category" :options="categoryOptions" width="130px" @change="fetchWords" />
      <BaseSelect v-model="difficulty" :options="difficultyOptions" width="120px" @change="fetchWords" />
      <button class="btn btn-primary btn-sm" @click="$router.push('/study/flashcard')">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="2 10 22 10"/></svg>
        闪卡学习
      </button>
    </div>

    <!-- 单词列表 -->
    <div class="word-list" v-if="words.length">
      <WordCard
        v-for="word in words" :key="word.id" :word="word"
        @click="$router.push(`/vocabulary/${word.id}`)"
        @toggleFavorite="() => handleToggleFavorite(word)"
        @markMastered="() => handleMarkMastered(word)"
      />
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="totalPages > 1">
      <button class="btn btn-ghost btn-sm" :disabled="page <= 1" @click="goPage(page - 1)">上一页</button>
      <span class="page-info">第 {{ page }} / {{ totalPages }} 页（共 {{ total }} 个单词）</span>
      <button class="btn btn-ghost btn-sm" :disabled="!hasNext" @click="goPage(page + 1)">下一页</button>
    </div>

    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div class="empty-state" v-if="!loading && words.length === 0">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <p>没有找到匹配的单词</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { vocabularyAPI } from '@/api'
import WordCard from '@/components/WordCard.vue'
import BaseSelect from '@/components/BaseSelect.vue'

const words = ref([])
const search = ref('')
const category = ref('')
const difficulty = ref('')

const categoryOptions = [
  { value: '', label: '全部分类' },
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

const difficultyOptions = [
  { value: '', label: '全部难度' },
  { value: '1', label: '★' },
  { value: '2', label: '★★' },
  { value: '3', label: '★★★' },
  { value: '4', label: '★★★★' },
  { value: '5', label: '★★★★★' }
]
const page = ref(1)
const total = ref(0)
const totalPages = ref(1)
const hasNext = ref(false)
const loading = ref(true)
let timer = null

function debouncedSearch() {
  clearTimeout(timer)
  timer = setTimeout(() => fetchWords(), 300)
}

async function fetchWords() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (search.value) params.search = search.value
    if (category.value) params.category = category.value
    if (difficulty.value) params.difficulty = difficulty.value
    const res = await vocabularyAPI.getWords(params)
    words.value = res.data.results
    total.value = res.data.count
    totalPages.value = Math.ceil(total.value / 20)
    hasNext.value = !!res.data.next
  } catch (e) {
    console.error('加载词汇失败', e)
  } finally {
    loading.value = false
  }
}

function goPage(p) {
  page.value = p
  fetchWords()
  window.scrollTo(0, 0)
}

async function handleToggleFavorite(word) {
  try {
    const res = await vocabularyAPI.toggleFavorite(word.id)
    word.is_favorite = res.data.is_favorite
  } catch (e) { console.error('操作失败', e) }
}

async function handleMarkMastered(word) {
  try {
    await vocabularyAPI.markMastered(word.id)
    word.mastered = true
  } catch (e) { console.error('操作失败', e) }
}

onMounted(() => fetchWords())
</script>

<style scoped>
.filters { display: flex; gap: 10px; margin-bottom: 20px; padding: 12px 16px; align-items: center; flex-wrap: wrap; }
.search-wrap {
  flex: 1; min-width: 180px;
  display: flex; align-items: center; gap: 8px;
  background: var(--bg-input);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0 12px;
}
.search-wrap svg { color: var(--text-muted); flex-shrink: 0; }
.search-input {
  width: 100%; padding: 10px 0; border: none; outline: none;
  background: transparent; color: var(--text); font-size: 14px;
}
.word-list { display: flex; flex-direction: column; gap: 10px; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 28px; }
.page-info { font-size: 13px; color: var(--text-muted); }
</style>
