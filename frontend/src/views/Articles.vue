<template>
  <div class="container">
    <div class="page-header">
      <h1>文章阅读</h1>
      <p>在真实语境中提升英语阅读能力</p>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <div class="search-wrap">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input v-model="search" class="search-input" placeholder="搜索文章标题..." @input="onSearch" />
      </div>
      <div class="level-filters">
        <button v-for="l in levels" :key="l.value" :class="['filter-btn', { active: currentLevel === l.value }]" @click="filterLevel(l.value)">
          {{ l.label }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading"><div class="spinner"></div><p>加载中...</p></div>

    <!-- 文章网格 -->
    <div v-else-if="articles.length" class="article-grid">
      <router-link v-for="article in articles" :key="article.id" :to="`/articles/${article.id}`" class="article-card card card-interactive">
        <div class="article-level">
          <span :class="['badge', levelBadge(article.level)]">{{ levelLabel(article.level) }}</span>
          <span class="word-count">{{ article.word_count }} 词</span>
        </div>
        <h2 class="article-title">{{ article.title }}</h2>
        <p class="article-title-cn" v-if="article.title_cn">{{ article.title_cn }}</p>
        <p class="article-summary">{{ article.summary }}</p>
        <div class="article-meta">
          <span class="tags" v-if="article.tags">
            <span v-for="tag in article.tags.split(',')" :key="tag" class="tag">#{{ tag.trim() }}</span>
          </span>
          <span class="meta-right">
            <span class="read-count">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              {{ article.read_count }}
            </span>
            <span>{{ formatDate(article.created_at) }}</span>
          </span>
        </div>
      </router-link>
    </div>

    <div v-else class="empty-state">
      <p v-if="currentLevel">该难度下暂无文章</p>
      <p v-else-if="search">未搜索到相关文章</p>
      <p v-else>暂无文章</p>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > pageSize">
      <button class="btn btn-ghost btn-sm" :disabled="!hasPrev" @click="goPage(currentPage - 1)">上一页</button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button class="btn btn-ghost btn-sm" :disabled="!hasNext" @click="goPage(currentPage + 1)">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { articleAPI } from '@/api'

const articles = ref([])
const levels = ref([])
const loading = ref(true)
const search = ref('')
const currentLevel = ref('')
const currentPage = ref(1)
const total = ref(0)
const pageSize = 6

const totalPages = computed(() => Math.ceil(total.value / pageSize) || 1)
const hasPrev = computed(() => currentPage.value > 1)
const hasNext = computed(() => currentPage.value < totalPages.value)

const levelLabels = { beginner: '入门', intermediate: '中级', advanced: '高级' }
const levelBadgeClass = { beginner: 'badge-success', intermediate: 'badge-warning', advanced: 'badge-danger' }

function levelLabel(l) { return levelLabels[l] || l }
function levelBadge(l) { return levelBadgeClass[l] || 'badge-accent' }
function formatDate(d) { if (!d) return ''; return new Date(d).toLocaleDateString('zh-CN') }

async function fetchArticles() {
  loading.value = true
  try {
    const params = { page: currentPage.value, page_size: pageSize }
    if (currentLevel.value) params.level = currentLevel.value
    if (search.value) params.search = search.value
    const res = await articleAPI.getList(params)
    articles.value = res.data.results || res.data
    total.value = res.data.count || 0
  } catch (e) { console.error('加载失败', e) }
  finally { loading.value = false }
}

function filterLevel(level) {
  currentLevel.value = currentLevel.value === level ? '' : level
  currentPage.value = 1; fetchArticles()
}

let searchTimer
function onSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { currentPage.value = 1; fetchArticles() }, 400)
}
function goPage(p) { currentPage.value = p; fetchArticles(); window.scrollTo({ top: 0, behavior: 'smooth' }) }

onMounted(async () => {
  try { const res = await articleAPI.getLevels(); levels.value = Object.entries(res.data).map(([v, l]) => ({ value: v, label: l })) }
  catch (e) { levels.value = [{ value: 'beginner', label: '入门' }, { value: 'intermediate', label: '中级' }, { value: 'advanced', label: '高级' }] }
  fetchArticles()
})
</script>

<style scoped>
.filter-bar { display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 24px; align-items: center; }
.search-wrap {
  flex: 1; min-width: 200px; max-width: 360px;
  display: flex; align-items: center; gap: 8px;
  background: var(--bg-input); border: 1.5px solid var(--border);
  border-radius: var(--radius-sm); padding: 0 12px;
}
.search-wrap svg { color: var(--text-muted); flex-shrink: 0; }
.search-input { width: 100%; padding: 10px 0; border: none; outline: none; background: transparent; color: var(--text); font-size: 14px; }
.level-filters { display: flex; gap: 6px; }
.filter-btn {
  padding: 7px 14px; border-radius: var(--radius-sm); font-size: 13px; font-weight: 500;
  background: var(--bg-card); color: var(--text-secondary);
  border: 1.5px solid var(--border); cursor: pointer; transition: all var(--transition);
}
.filter-btn:hover { border-color: var(--accent); color: var(--accent); }
.filter-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }

.article-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 18px; }
@media (max-width: 480px) { .article-grid { grid-template-columns: 1fr; } }
.article-card {
  display: flex; flex-direction: column; min-height: 220px;
  cursor: pointer; text-decoration: none; color: inherit;
}
.article-level { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.word-count { font-size: 12px; color: var(--text-muted); }
.article-title { font-family: var(--font-heading); font-size: 18px; font-weight: 700; color: var(--text); line-height: 1.35; margin-bottom: 6px; letter-spacing: -0.01em; }
.article-title-cn { font-size: 13px; color: var(--text-secondary); margin-bottom: 10px; }
.article-summary { font-size: 13px; color: var(--text-muted); line-height: 1.5; flex: 1; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.article-meta { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--border); font-size: 12px; color: var(--text-muted); }
.tags { display: flex; gap: 6px; flex-wrap: wrap; }
.tag { color: var(--accent); }
.meta-right { display: flex; gap: 12px; align-items: center; }
.read-count { display: flex; align-items: center; gap: 4px; }
.pagination { display: flex; justify-content: center; align-items: center; gap: 16px; margin-top: 32px; padding-bottom: 40px; }
.page-info { font-size: 13px; color: var(--text-secondary); }
</style>
