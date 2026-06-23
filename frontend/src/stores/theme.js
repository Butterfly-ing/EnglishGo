import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STYLES = [
  { id: 'future',   name: '未来风',  desc: '赛博霓虹 · 科技质感', defaultMode: 'dark' },
  { id: 'retro',    name: '怀旧风',  desc: '复古暖色 · 时光质感', defaultMode: 'light' },
  { id: 'classic',  name: '经典风',  desc: '简约专业 · 清爽有序', defaultMode: 'light' },
  { id: 'book',     name: '书籍风',  desc: '温润纸张 · 沉浸阅读', defaultMode: 'light' },
  { id: 'literary', name: '文艺风',  desc: '优雅柔和 · 艺术气息', defaultMode: 'light' },
]

const PRESET_COLORS = [
  '#00d4ff', '#00e676', '#2563eb', '#7b61ff',
  '#c0392b', '#e67e22', '#5b3e2e', '#9b59b6',
  '#ff5252', '#ffab00', '#059669', '#0ea5e9',
]

function loadSetting(key, fallback) {
  try {
    const v = localStorage.getItem(key)
    return v || fallback
  } catch { return fallback }
}

function saveSetting(key, value) {
  try { localStorage.setItem(key, value) } catch {}
}

export const useThemeStore = defineStore('theme', () => {
  // 当前主题风格
  const style = ref(loadSetting('theme_style', 'future'))
  // 深色/浅色模式 (dark / light)
  const darkMode = ref(loadSetting('theme_darkMode', 'true') === 'true')
  // 自定义强调色（空 = 使用主题自带）
  const accentColor = ref(loadSetting('theme_accent', ''))
  // 字体大小
  const fontSize = ref(Number(loadSetting('theme_fontSize', '16')))

  function apply() {
    const root = document.documentElement
    // 设置主题风格
    root.setAttribute('data-theme-style', style.value)
    // 设置深色/浅色模式
    root.setAttribute('data-theme-mode', darkMode.value ? 'dark' : 'light')
    // 自定义强调色
    if (accentColor.value) {
      root.style.setProperty('--accent', accentColor.value)
      const r = parseInt(accentColor.value.slice(1,3), 16)
      const g = parseInt(accentColor.value.slice(3,5), 16)
      const b = parseInt(accentColor.value.slice(5,7), 16)
      root.style.setProperty('--accent-glow', `0 0 24px rgba(${r},${g},${b},0.25)`)
      root.style.setProperty('--border-accent', `rgba(${r},${g},${b},0.3)`)
    } else {
      root.style.removeProperty('--accent')
      root.style.removeProperty('--accent-glow')
      root.style.removeProperty('--border-accent')
    }
    // 字体大小
    root.style.setProperty('font-size', fontSize.value + 'px')

    saveSetting('theme_style', style.value)
    saveSetting('theme_darkMode', String(darkMode.value))
    saveSetting('theme_accent', accentColor.value)
    saveSetting('theme_fontSize', String(fontSize.value))
  }

  function setStyle(id) {
    style.value = id
    // 保留用户当前的深色/浅色偏好，不自动重置
    apply()
  }

  function toggleDarkMode() {
    darkMode.value = !darkMode.value
    apply()
  }

  function setDarkMode(val) {
    darkMode.value = val
    apply()
  }

  function setAccent(color) {
    accentColor.value = color
    apply()
  }

  function resetAccent() {
    accentColor.value = ''
    apply()
  }

  function setFontSize(size) {
    fontSize.value = size
    apply()
  }

  // 初始化
  apply()

  return {
    style, darkMode, accentColor, fontSize,
    STYLES, PRESET_COLORS,
    setStyle, toggleDarkMode, setDarkMode,
    setAccent, resetAccent, setFontSize,
    apply,
  }
})
