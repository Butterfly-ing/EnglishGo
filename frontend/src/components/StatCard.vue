<template>
  <div class="stat-card card">
    <div class="stat-icon" :style="{ background: bgColor + '18', color: bgColor }">
      <slot name="icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/></svg>
      </slot>
    </div>
    <div class="stat-info">
      <div class="stat-value">{{ value }}</div>
      <div class="stat-label">{{ label }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  value: [String, Number],
  label: String,
  bgColor: { type: String, default: '#00d4ff' }
})
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  animation: fadeIn 0.4s ease;
}
.stat-icon {
  width: 46px;
  height: 46px;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all var(--transition);
}
.stat-value {
  font-family: var(--font-heading);
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
  color: var(--text);
}
.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
</style>
