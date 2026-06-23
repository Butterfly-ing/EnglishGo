<template>
  <div class="container">
    <div v-if="loading" class="loading"><div class="spinner"></div><p>加载中...</p></div>

    <template v-else-if="article">
      <router-link to="/articles" class="back-link">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        返回文章列表
      </router-link>

      <!-- 头部 -->
      <div class="article-header">
        <div class="header-top">
          <span :class="['badge', levelBadge(article.level)]">{{ levelLabel(article.level) }}</span>
          <span class="word-count">{{ article.word_count }} 词</span>
        </div>
        <h1 class="article-title">{{ article.title }}</h1>
        <p class="article-title-cn" v-if="article.title_cn">{{ article.title_cn }}</p>
        <div class="header-meta">
          <span>{{ article.author }}</span>
          <span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            {{ article.read_count }} 阅读
          </span>
          <span>{{ formatDate(article.created_at) }}</span>
          <span v-if="article.tags" class="header-tags">
            <span v-for="tag in article.tags.split(',')" :key="tag" class="tag">#{{ tag.trim() }}</span>
          </span>
        </div>
      </div>

      <!-- 正文 -->
      <div class="article-body card">
        <div class="content-blocks">
          <div v-for="(paragraph, idx) in paragraphs" :key="idx" class="paragraph-block">
            <div class="english-text" @mouseenter="hoveredPara = idx" @mouseleave="hoveredPara = -1">
              <template v-for="(word, wi) in paragraph.words" :key="wi">
                <span :class="['clickable-word', { highlighted: hoveredWord?.para === idx && hoveredWord?.idx === wi }]" @click="lookupWord(word, idx, wi)">{{ word.text }}</span>
              </template>
            </div>
            <div v-if="hoveredPara === idx && paragraph.cn" class="chinese-text">{{ paragraph.cn }}</div>
          </div>
        </div>
      </div>

      <!-- 全文翻译 -->
      <div v-if="article.content_cn" class="translation-section card">
        <div class="ts-header">
          <span class="ts-title">全文翻译</span>
          <button class="btn btn-ghost btn-sm" @click="showFullCN = !showFullCN">{{ showFullCN ? '隐藏翻译' : '显示翻译' }}</button>
        </div>
        <div v-if="showFullCN" class="full-translation">
          <p v-for="(p, i) in cnParagraphs" :key="i" class="cn-para">{{ p }}</p>
        </div>
      </div>

      <!-- 查词弹窗 -->
      <div v-if="lookupResult" class="lookup-popup" :style="lookupStyle">
        <div class="lookup-word">{{ lookupResult.word }}</div>
        <div class="lookup-meaning">{{ lookupResult.meaning }}</div>
        <button class="lookup-close" @click="lookupResult = null">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
    </template>

    <div v-else class="empty-state">
      <p>文章不存在或已被删除</p>
      <router-link to="/articles" class="btn btn-primary" style="margin-top:12px">返回文章列表</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { articleAPI, vocabularyAPI } from '@/api'

const route = useRoute()
const article = ref(null)
const loading = ref(true)
const showFullCN = ref(false)
const hoveredPara = ref(-1)
const hoveredWord = ref(null)
const lookupResult = ref(null)
const lookupStyle = reactive({ top: '0px', left: '0px' })

const levelLabels = { beginner: '入门', intermediate: '中级', advanced: '高级' }
const levelBadgeClass = { beginner: 'badge-success', intermediate: 'badge-warning', advanced: 'badge-danger' }

function levelLabel(l) { return levelLabels[l] || l }
function levelBadge(l) { return levelBadgeClass[l] || 'badge-accent' }
function formatDate(d) { if (!d) return ''; return new Date(d).toLocaleDateString('zh-CN') }

const paragraphs = computed(() => {
  if (!article.value) return []
  const enParas = article.value.content.split('\n').filter(p => p.trim())
  const cnParas = article.value.content_cn ? article.value.content_cn.split('\n').filter(p => p.trim()) : []
  return enParas.map((para, i) => ({
    words: para.split(/(?<=\s)(?=\S)/).map(w => ({ text: w, clean: w.replace(/[.,!?;:'"()]+$/, '') })),
    cn: cnParas[i] || ''
  }))
})
const cnParagraphs = computed(() => {
  if (!article.value?.content_cn) return []
  return article.value.content_cn.split('\n').filter(p => p.trim())
})

async function lookupWord(word, paraIdx, wordIdx) {
  const clean = word.clean.replace(/[^a-zA-Z\s-]/g, '').toLowerCase()
  if (clean.length < 2) { lookupResult.value = { word: word.text, meaning: '标点或短词' }; return }
  try {
    const res = await vocabularyAPI.getWords({ search: clean })
    if (res.data.results?.length > 0) {
      const w = res.data.results[0]
      lookupResult.value = { word: w.english, meaning: `${w.chinese}  ${w.part_of_speech ? '[' + w.part_of_speech + ']' : ''}` }
    } else { lookupResult.value = { word: clean, meaning: '未找到释义' } }
  } catch { lookupResult.value = { word: clean, meaning: '查询失败' } }
  hoveredWord.value = { para: paraIdx, idx: wordIdx }
}

document.addEventListener('click', (e) => {
  if (lookupResult.value && e.target.classList.contains('clickable-word')) {
    const rect = e.target.getBoundingClientRect()
    lookupStyle.top = `${rect.bottom + window.scrollY + 8}px`
    lookupStyle.left = `${rect.left + window.scrollX}px`
  } else if (lookupResult.value && !e.target.closest('.lookup-popup')) {
    lookupResult.value = null; hoveredWord.value = null
  }
})

onMounted(async () => {
  loading.value = true
  try { const res = await articleAPI.getDetail(route.params.id); article.value = res.data }
  catch (e) { console.error('加载失败', e) }
  finally { loading.value = false }
})
</script>

<style scoped>
.back-link { display: inline-flex; align-items: center; gap: 4px; margin-bottom: 20px; color: var(--text-secondary); font-size: 13px; transition: color var(--transition); }
.back-link:hover { color: var(--accent); }

.article-header { margin-bottom: 24px; }
.header-top { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.word-count { font-size: 13px; color: var(--text-muted); }
.article-title { font-family: var(--font-heading); font-size: 28px; font-weight: 800; color: var(--text); line-height: 1.3; margin-bottom: 8px; letter-spacing: -0.02em; }
.article-title-cn { font-size: 15px; color: var(--text-secondary); margin-bottom: 14px; }
.header-meta { display: flex; flex-wrap: wrap; gap: 16px; font-size: 13px; color: var(--text-muted); align-items: center; }
.header-meta span { display: flex; align-items: center; gap: 4px; }
.header-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.tag { color: var(--accent); }

.article-body { margin-bottom: 20px; padding: 36px; }
.paragraph-block { margin-bottom: 22px; }
.paragraph-block:last-child { margin-bottom: 0; }
.english-text { font-size: 17px; line-height: 2; color: var(--text); cursor: default; }
.clickable-word { cursor: pointer; border-radius: 3px; transition: all 0.15s; padding: 0 1px; }
.clickable-word:hover { background: rgba(0,212,255,0.12); color: var(--accent); }
.clickable-word.highlighted { background: rgba(0,212,255,0.18); color: var(--accent); }
.chinese-text {
  margin-top: 8px; padding: 10px 16px;
  background: var(--bg-hover); border-radius: var(--radius-sm);
  font-size: 14px; color: var(--text-secondary); line-height: 1.7;
  border-left: 3px solid var(--accent);
}

.translation-section { margin-bottom: 40px; }
.ts-header { display: flex; justify-content: space-between; align-items: center; }
.ts-title { font-family: var(--font-heading); font-size: 16px; font-weight: 600; color: var(--text); }
.full-translation { margin-top: 16px; padding: 20px; background: var(--bg-hover); border-radius: var(--radius); }
.cn-para { font-size: 15px; line-height: 1.8; color: var(--text); margin-bottom: 12px; }
.cn-para:last-child { margin-bottom: 0; }

.lookup-popup {
  position: absolute; z-index: 200;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius); box-shadow: var(--shadow-lg);
  padding: 14px 20px; min-width: 180px; max-width: 300px;
}
.lookup-word { font-size: 16px; font-weight: 700; color: var(--accent); margin-bottom: 6px; }
.lookup-meaning { font-size: 14px; color: var(--text); line-height: 1.5; }
.lookup-close { position: absolute; top: 6px; right: 8px; background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 4px; }
.lookup-close:hover { color: var(--text); }

@media (max-width: 768px) {
  .article-title { font-size: 22px; }
  .article-body { padding: 20px; }
  .english-text { font-size: 15px; }
}
</style>
