<template>
  <div class="word-card card card-interactive" @click="$emit('click')">
    <div class="word-header">
      <div>
        <span class="word-english">{{ word.english }}</span>
        <span class="word-phonetic" v-if="word.phonetic">{{ word.phonetic }}</span>
      </div>
      <div class="word-actions" @click.stop>
        <button class="icon-btn" :class="{ active: word.is_favorite }" @click="$emit('toggleFavorite')" :title="word.is_favorite ? '取消收藏' : '收藏'">
          <svg width="16" height="16" viewBox="0 0 24 24" :fill="word.is_favorite ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
        </button>
        <button class="icon-btn" :class="{ active: word.mastered }" @click="$emit('markMastered')" :title="word.mastered ? '已掌握' : '标记掌握'">
          <svg width="16" height="16" viewBox="0 0 24 24" :fill="word.mastered ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        </button>
      </div>
    </div>
    <div class="word-chinese">{{ word.chinese }}</div>
    <div class="word-meta">
      <span class="badge badge-accent">{{ posName }}</span>
      <span class="badge" :class="diffBadgeClass">{{ '★'.repeat(word.difficulty || 1) }}</span>
      <span class="badge badge-success" v-if="word.category">{{ catName }}</span>
    </div>
    <div class="word-example" v-if="word.example">
      {{ word.example }}
    </div>
    <div class="word-stats" v-if="word.practice_count > 0">
      练习 {{ word.practice_count }} 次  ·  正确 {{ word.correct_count }} 次
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ word: Object })
defineEmits(['click', 'toggleFavorite', 'markMastered'])

const categoryMap = {
  junior: '初中', senior: '高中', cet4: '四级', cet6: '六级',
  postgraduate:'考研', toefl: '托福', sat: 'SAT',
  basic: '基础', intermediate: '中级', advanced: '高级',
  business: '商务', travel: '旅游'
}
const posMap = { noun: '名词', verb: '动词', adjective: '形容词', adverb: '副词', preposition: '介词', conjunction: '连词', pronoun: '代词', phrase: '短语' }

const posName = computed(() => posMap[props.word.part_of_speech] || props.word.part_of_speech)
const catName = computed(() => categoryMap[props.word.category] || props.word.category)
const diffBadgeClass = computed(() => (props.word.difficulty || 1) <= 2 ? 'badge-success' : (props.word.difficulty <= 3 ? 'badge-warning' : 'badge-danger'))
</script>

<style scoped>
.word-card { padding: 20px; }
.word-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
.word-english { font-family: var(--font-heading); font-size: 19px; font-weight: 700; color: var(--text); letter-spacing: -0.01em; }
.word-phonetic { font-size: 13px; color: var(--text-muted); margin-left: 8px; }
.word-chinese { font-size: 15px; color: var(--text-secondary); margin-top: 4px; }
.word-meta { display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
.word-example {
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-secondary);
  font-style: italic;
  background: var(--bg-hover);
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  border-left: 3px solid var(--border-accent);
}
.word-stats { margin-top: 10px; font-size: 12px; color: var(--text-muted); }
.word-actions { display: flex; gap: 2px; }
.icon-btn {
  width: 32px; height: 32px;
  border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center;
  background: transparent;
  color: var(--text-muted);
  transition: all var(--transition);
}
.icon-btn:hover { background: var(--bg-hover); color: var(--text); }
.icon-btn.active { color: var(--accent); }
</style>
