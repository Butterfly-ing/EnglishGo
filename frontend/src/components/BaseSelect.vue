<template>
  <div class="base-select" ref="rootEl" :style="{ width: width || '100%' }">
    <button
      class="select-trigger"
      @click="open = !open"
      @keydown.escape="open = false"
      type="button"
    >
      <span class="select-label" :class="{ placeholder: !selectedLabel }">
        {{ selectedLabel || placeholder }}
      </span>
      <svg
        class="select-arrow"
        :class="{ open }"
        width="12" height="12" viewBox="0 0 12 12"
      >
        <path fill="currentColor" d="M6 8L1 3h10z" />
      </svg>
    </button>
    <Teleport to="body">
      <div class="select-dropdown" :class="{ open }" :style="dropdownStyle" v-if="open" ref="dropdownEl">
        <button
          v-for="opt in options"
          :key="opt.value"
          class="select-option"
          :class="{
            selected: modelValue === opt.value,
            disabled: opt.disabled
          }"
          :disabled="opt.disabled"
          @click="select(opt)"
          type="button"
        >
          {{ opt.label }}
          <svg v-if="modelValue === opt.value && !opt.disabled" class="check-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
        </button>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, required: true },
  placeholder: { type: String, default: '请选择' },
  width: { type: String, default: '' }
})

const emit = defineEmits(['update:modelValue', 'change'])

const open = ref(false)
const rootEl = ref(null)
const dropdownEl = ref(null)
const dropdownStyle = ref({})

const selectedLabel = computed(() => {
  const opt = props.options.find(o => o.value === props.modelValue)
  return opt ? opt.label : ''
})

function select(opt) {
  if (opt.disabled) return
  emit('update:modelValue', opt.value)
  emit('change', opt.value)
  open.value = false
}

function calcPosition() {
  if (!rootEl.value) return
  const rect = rootEl.value.getBoundingClientRect()
  dropdownStyle.value = {
    position: 'fixed',
    top: rect.bottom + 4 + 'px',
    left: rect.left + 'px',
    width: rect.width + 'px',
    zIndex: 9999
  }
}

function handleClickOutside(e) {
  if (rootEl.value && !rootEl.value.contains(e.target)) {
    // Check if click was inside dropdown (teleported to body)
    if (dropdownEl.value && !dropdownEl.value.contains(e.target)) {
      open.value = false
    }
  }
}

watch(open, async (val) => {
  if (val) {
    await nextTick()
    calcPosition()
  }
})

onMounted(() => {
  document.addEventListener('click', handleClickOutside, true)
  window.addEventListener('resize', calcPosition)
  window.addEventListener('scroll', calcPosition, true)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside, true)
  window.removeEventListener('resize', calcPosition)
  window.removeEventListener('scroll', calcPosition, true)
})
</script>

<style scoped>
.base-select { position: relative; }

.select-trigger {
  width: 100%;
  padding: 10px 16px;
  border: var(--border-width, 1.5px) var(--border-style, solid) var(--border);
  border-radius: var(--radius-sm, 8px);
  font-size: 14px;
  background: var(--bg-input, #fff);
  color: var(--text, #333);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  transition: all var(--transition, 0.2s ease);
  outline: none;
  font-family: inherit;
  text-align: left;
}
.select-trigger:hover {
  border-color: var(--accent);
}
.select-trigger:focus-visible {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(0,212,255,0.08);
}

.select-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text);
}
.select-label.placeholder {
  color: var(--text-muted, #999);
}

.select-arrow {
  flex-shrink: 0;
  color: var(--text-muted, #999);
  transition: transform 0.2s ease;
}
.select-arrow.open { transform: rotate(180deg); }

.select-dropdown {
  position: fixed;
  z-index: 9999;
  background: var(--bg-card, #fff);
  border: var(--border-width, 1.5px) var(--border-style, solid) var(--border);
  border-radius: var(--radius-sm, 8px);
  box-shadow: var(--shadow-lg, 0 8px 32px rgba(0,0,0,0.15));
  max-height: 260px;
  overflow-y: auto;
  padding: 4px;
  display: none;
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
}
.select-dropdown.open { display: block; }

.select-option {
  width: 100%;
  padding: 9px 12px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--text);
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-align: left;
  font-family: inherit;
  transition: background 0.12s ease;
}
.select-option:hover:not(.disabled) {
  background: var(--bg-hover, rgba(0,0,0,0.04));
}
.select-option.selected {
  color: var(--accent);
  font-weight: 600;
}
.select-option.disabled {
  color: var(--text-muted, #999);
  cursor: default;
  font-size: 12px;
  letter-spacing: 0.1em;
  padding: 6px 12px;
  pointer-events: none;
}
.select-option.disabled::before {
  content: '';
  display: none;
}

.check-icon {
  flex-shrink: 0;
  margin-left: 8px;
}
</style>
