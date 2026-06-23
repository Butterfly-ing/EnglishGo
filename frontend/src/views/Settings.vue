<template>
  <div class="container">
    <div class="page-header">
      <h1>设置</h1>
      <p>个性化你的学习体验</p>
    </div>

    <div class="settings-layout">
      <!-- 左侧导航 -->
      <div class="settings-sidebar card">
        <button
          v-for="tab in tabs" :key="tab.id"
          :class="['sb-item', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          <span v-html="tab.icon"></span>
          {{ tab.label }}
        </button>
      </div>

      <!-- 右侧内容 -->
      <div class="settings-content">

        <!-- 主题风格 -->
        <div v-if="activeTab === 'theme'" class="card setting-section">
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
            主题风格
          </h2>
          <p class="section-desc">选择一套完整的视觉风格，改变整体界面感受</p>
          <div class="theme-grid">
            <button
              v-for="t in theme.STYLES" :key="t.id"
              :class="['theme-card', { active: theme.style === t.id }]"
              @click="theme.setStyle(t.id)"
            >
              <div :class="['theme-preview', 'preview-' + t.id]" :data-mode="theme.style === t.id ? (theme.darkMode ? 'dark' : 'light') : t.defaultMode">
                <div class="tp-bar"></div>
                <div class="tp-line"></div>
                <div class="tp-line short"></div>
              </div>
              <div class="theme-info">
                <div class="theme-name">{{ t.name }}</div>
                <div class="theme-desc">{{ t.desc }}</div>
              </div>
              <div v-if="theme.style === t.id" class="theme-check">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
            </button>
          </div>
        </div>

        <!-- 显示模式 -->
        <div v-if="activeTab === 'display'" class="card setting-section">
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            显示模式
          </h2>
          <p class="section-desc">
            当前主题「{{ currentStyleName }}」，切换深色/浅色不会改变主题风格
          </p>
          <div class="display-modes">
            <button
              :class="['mode-card', { active: !theme.darkMode }]"
              @click="theme.setDarkMode(false)"
            >
              <div class="mode-icon light-icon">
                <div class="mode-sun"></div>
              </div>
              <div class="mode-label">浅色模式</div>
              <div class="mode-hint">适用于「{{ currentStyleName }}」主题</div>
            </button>
            <button
              :class="['mode-card', { active: theme.darkMode }]"
              @click="theme.setDarkMode(true)"
            >
              <div class="mode-icon dark-icon">
                <div class="mode-moon"></div>
              </div>
              <div class="mode-label">深色模式</div>
              <div class="mode-hint">适用于「{{ currentStyleName }}」主题</div>
            </button>
          </div>
        </div>

        <!-- 强调色 -->
        <div v-if="activeTab === 'color'" class="card setting-section">
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/></svg>
            强调色
          </h2>
          <p class="section-desc">自定义界面的强调色，覆盖主题默认色</p>
          <div class="color-row">
            <button
              v-for="c in theme.PRESET_COLORS" :key="c"
              :class="['color-dot', { active: theme.accentColor === c }]"
              :style="{ background: c }"
              @click="theme.accentColor === c ? theme.resetAccent() : theme.setAccent(c)"
            ></button>
            <!-- 自定义拾色器 -->
            <label class="color-dot custom" :style="{ background: customColor || '#ccc' }">
              <span>+</span>
              <input type="color" v-model="customColor" @change="theme.setAccent($event.target.value)" />
            </label>
          </div>
          <button v-if="theme.accentColor" class="btn btn-ghost btn-sm" style="margin-top:16px" @click="theme.resetAccent()">
            恢复主题默认色
          </button>
        </div>

        <!-- 字体 -->
        <div v-if="activeTab === 'font'" class="card setting-section">
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>
            字体大小
          </h2>
          <p class="section-desc">调整全局字体大小，适配你的阅读偏好</p>
          <div class="font-controls">
            <button class="btn btn-ghost btn-sm" @click="theme.setFontSize(Math.max(12, theme.fontSize - 1))">A-</button>
            <div class="font-preview" :style="{ fontSize: theme.fontSize + 'px' }">
              预览文字 Preview
            </div>
            <button class="btn btn-ghost btn-sm" @click="theme.setFontSize(Math.min(24, theme.fontSize + 1))">A+</button>
          </div>
          <div class="font-size-label">{{ theme.fontSize }}px</div>
        </div>

        <!-- 关于 -->
        <div v-if="activeTab === 'about'" class="card setting-section">
          <h2 class="section-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            关于 EnglishGo
          </h2>
          <div class="about-info">
            <div class="about-item">
              <span class="about-label">版本</span>
              <span class="about-value">1.0.0</span>
            </div>
            <div class="about-item">
              <span class="about-label">技术栈</span>
              <span class="about-value">Vue 3 · Django · MySQL</span>
            </div>
            <div class="about-item">
              <span class="about-label">功能</span>
              <span class="about-value">词汇学习 · 闪卡记忆 · 测验练习 · 文章阅读</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

const theme = useThemeStore()
const activeTab = ref('theme')
const customColor = ref('#00d4ff')

const currentStyleName = computed(() => {
  const s = theme.STYLES.find(s => s.id === theme.style)
  return s ? s.name : '未知'
})

const tabs = [
  {
    id: 'theme',
    label: '主题风格',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
  },
  {
    id: 'display',
    label: '显示模式',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
  },
  {
    id: 'color',
    label: '强调色',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/></svg>',
  },
  {
    id: 'font',
    label: '字体',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>',
  },
  {
    id: 'about',
    label: '关于',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
  },
]
</script>

<style scoped>
.settings-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 28px;
  align-items: start;
}
@media (max-width: 768px) {
  .settings-layout { grid-template-columns: 1fr; }
}

/* ---- 侧边栏 ---- */
.settings-sidebar {
  padding: 12px;
  position: sticky;
  top: 80px;
}
.sb-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  transition: all var(--transition);
  text-align: left;
}
.sb-item:hover {
  background: var(--bg-hover);
  color: var(--text);
}
.sb-item.active {
  background: var(--accent);
  color: #fff;
}
.sb-item :deep(svg) { flex-shrink: 0; }

/* ---- 内容区 ---- */
.settings-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.setting-section {
  animation: fadeIn 0.4s ease;
}
.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--text);
}
.section-title :deep(svg) { color: var(--accent); }
.section-desc {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 24px;
}

/* ---- 主题卡片网格 ---- */
.theme-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 14px;
}
.theme-card {
  position: relative;
  padding: 16px;
  border-radius: var(--radius);
  border: 2px solid var(--border);
  background: var(--bg-card-solid);
  cursor: pointer;
  transition: all var(--transition);
  text-align: left;
}
.theme-card:hover { border-color: var(--border-accent); }
.theme-card.active {
  border-color: var(--accent);
  box-shadow: 0 0 0 4px rgba(0,212,255,0.06);
}
.theme-check {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 主题预览微缩图 */
.theme-preview {
  height: 60px;
  border-radius: 6px;
  margin-bottom: 12px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.tp-bar { height: 8px; border-radius: 4px; width: 40%; }
.tp-line { height: 4px; border-radius: 2px; width: 70%; }
.tp-line.short { width: 45%; }

/* 预览用深/浅色底色 */
.theme-preview[data-mode="dark"]  { background: #111; }
.theme-preview[data-mode="light"] { background: #f5f5f5; }

.preview-future[data-mode="dark"]  .tp-bar { background: #00d4ff; }
.preview-future[data-mode="dark"]  .tp-line { background: rgba(255,255,255,0.15); }
.preview-future[data-mode="light"] .tp-bar { background: #0284c7; }
.preview-future[data-mode="light"] .tp-line { background: rgba(0,0,0,0.1); }

.preview-retro[data-mode="dark"]  .tp-bar { background: #e74c3c; }
.preview-retro[data-mode="dark"]  .tp-line { background: rgba(255,255,255,0.12); }
.preview-retro[data-mode="light"] .tp-bar { background: #c0392b; }
.preview-retro[data-mode="light"] .tp-line { background: rgba(0,0,0,0.1); }

.preview-classic[data-mode="dark"]  .tp-bar { background: #60a5fa; }
.preview-classic[data-mode="dark"]  .tp-line { background: rgba(255,255,255,0.12); }
.preview-classic[data-mode="light"] .tp-bar { background: #2563eb; }
.preview-classic[data-mode="light"] .tp-line { background: rgba(0,0,0,0.1); }

.preview-book[data-mode="dark"]  .tp-bar { background: #c4956a; }
.preview-book[data-mode="dark"]  .tp-line { background: rgba(255,255,255,0.1); }
.preview-book[data-mode="light"] .tp-bar { background: #5b3e2e; }
.preview-book[data-mode="light"] .tp-line { background: rgba(0,0,0,0.08); }

.preview-literary[data-mode="dark"]  .tp-bar { background: #c084fc; }
.preview-literary[data-mode="dark"]  .tp-line { background: rgba(255,255,255,0.12); }
.preview-literary[data-mode="light"] .tp-bar { background: #9b59b6; }
.preview-literary[data-mode="light"] .tp-line { background: rgba(155,89,182,0.15); }

.theme-name { font-weight: 700; font-size: 14px; color: var(--text); }
.theme-desc { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

/* ---- 显示模式 ---- */
.display-modes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 14px;
}
.mode-card {
  padding: 24px 20px;
  border-radius: var(--radius);
  border: 2px solid var(--border);
  background: var(--bg-card-solid);
  cursor: pointer;
  transition: all var(--transition);
  text-align: center;
}
.mode-card:hover { border-color: var(--border-accent); }
.mode-card.active {
  border-color: var(--accent);
  box-shadow: 0 0 0 4px rgba(0,212,255,0.06);
}
.mode-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
}
.light-icon {
  background: #fff3cd;
}
.light-icon .mode-sun {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f59e0b;
  box-shadow: 0 0 16px rgba(245, 158, 11, 0.4);
}
.dark-icon {
  background: #1e293b;
}
.dark-icon .mode-moon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e2e8f0;
  box-shadow: 0 0 16px rgba(226, 232, 240, 0.2);
  position: relative;
}
.dark-icon .mode-moon::after {
  content: '';
  position: absolute;
  top: 2px;
  right: 2px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #1e293b;
}
.mode-label {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}
.mode-hint {
  font-size: 12px;
  color: var(--text-muted);
}

/* ---- 强调色 ---- */
.color-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}
.color-dot {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 3px solid transparent;
  cursor: pointer;
  transition: all var(--transition);
  flex-shrink: 0;
}
.color-dot:hover { transform: scale(1.15); }
.color-dot.active {
  border-color: var(--text);
  box-shadow: 0 0 0 4px rgba(0,0,0,0.1);
}
.color-dot.custom {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: #666;
  position: relative;
  overflow: hidden;
}
.color-dot.custom input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

/* ---- 字体 ---- */
.font-controls {
  display: flex;
  align-items: center;
  gap: 20px;
  justify-content: center;
  padding: 16px 0;
}
.font-preview {
  font-family: var(--font-body);
  font-weight: 700;
  color: var(--text);
  padding: 8px 20px;
  background: var(--bg-hover);
  border-radius: var(--radius-sm);
  transition: font-size 0.3s ease;
}
.font-size-label {
  text-align: center;
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 4px;
}

/* ---- 关于 ---- */
.about-info {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.about-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}
.about-item:last-child { border-bottom: none; }
.about-label { font-size: 13px; color: var(--text-muted); font-weight: 500; }
.about-value { font-size: 14px; color: var(--text); font-weight: 600; }
</style>
