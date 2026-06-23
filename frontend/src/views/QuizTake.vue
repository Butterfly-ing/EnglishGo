<template>
  <div class="container">
    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <p>正在生成题目...</p>
    </div>

    <div v-else-if="questions.length">
      <!-- 进度 -->
      <div class="qt-progress">
        <div class="progress-track"><div class="progress-fill" :style="{ width: progressPercent + '%' }"></div></div>
        <span class="prog-text">{{ currentIndex + 1 }} / {{ questions.length }}</span>
      </div>

      <!-- 题目 -->
      <div class="qt-question card" v-if="currentQuestion">
        <div class="qt-qnum">第 {{ currentIndex + 1 }} 题</div>
        <div class="qt-qtext">{{ currentQuestion.question }}</div>

        <!-- 选择题 -->
        <div class="qt-options" v-if="currentQuestion.question_type === 'choice'">
          <button
            v-for="(opt, i) in currentQuestion.options" :key="i"
            class="qt-option"
            :class="{ selected: userAnswer === opt, correct: submitted && opt === currentQuestion.correct_answer, wrong: submitted && userAnswer === opt && opt !== currentQuestion.correct_answer }"
            :disabled="submitted"
            @click="selectOption(opt)"
          >
            <span class="opt-letter">{{ 'ABCD'[i] }}</span>
            {{ opt }}
          </button>
        </div>

        <!-- 拼写 / 英译中 -->
        <div class="qt-input-area" v-else>
          <div class="qt-hint" v-if="currentQuestion.hint">提示: {{ currentQuestion.hint }}</div>
          <input
            v-model="userAnswer"
            class="form-input qt-input"
            :placeholder="currentQuestion.question_type === 'spelling' ? '请输入英文单词...' : '请输入中文意思...'"
            :disabled="submitted"
            @keyup.enter="submitAnswer"
          />
        </div>

        <div class="qt-feedback" v-if="submitted">
          <div class="feedback-line" :class="isCurrentCorrect ? 'correct' : 'wrong'">
            <svg v-if="isCurrentCorrect" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            {{ isCurrentCorrect ? '回答正确' : '回答错误' }}
          </div>
          <div class="feedback-answer" v-if="!isCurrentCorrect">
            正确答案：<strong>{{ currentQuestion.correct_answer }}</strong>
          </div>
        </div>
      </div>

      <!-- 操作 -->
      <div class="qt-actions">
        <button class="btn btn-primary" @click="submitAnswer" v-if="!submitted && userAnswer">确认答案</button>
        <button class="btn btn-primary" @click="nextQuestion" v-if="submitted">
          {{ currentIndex < questions.length - 1 ? '下一题' : '查看结果' }}
          <svg v-if="currentIndex < questions.length - 1" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </button>
        <button class="btn btn-ghost btn-sm" @click="$router.push('/quiz')" style="margin-left:auto">退出测验</button>
      </div>
    </div>

    <div class="empty-state" v-else>
      <p>无法生成题目，请检查单词库</p>
      <button class="btn btn-primary" @click="$router.push('/quiz')" style="margin-top:12px">返回</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { quizAPI, progressAPI } from '@/api'

const route = useRoute()
const router = useRouter()

const quizType = route.params.type
const loading = ref(true)
const questions = ref([])
const currentIndex = ref(0)
const userAnswer = ref('')
const submitted = ref(false)
const answers = ref([])

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)
const progressPercent = computed(() => questions.value.length ? ((currentIndex.value) / questions.value.length) * 100 : 0)
const isCurrentCorrect = computed(() => {
  if (!submitted.value || !currentQuestion.value) return false
  return userAnswer.value.trim().toLowerCase() === currentQuestion.value.correct_answer.trim().toLowerCase()
})

function selectOption(opt) { if (!submitted.value) userAnswer.value = opt }
function submitAnswer() {
  if (!userAnswer.value || submitted.value) return
  submitted.value = true
  answers.value.push({ question_id: currentQuestion.value.id, answer: userAnswer.value })
}
function nextQuestion() {
  if (currentIndex.value < questions.value.length - 1) { currentIndex.value++; userAnswer.value = ''; submitted.value = false }
  else submitQuiz()
}
async function submitQuiz() {
  try {
    const res = await quizAPI.submit({ quiz_type: quizType, total_questions: questions.value.length, answers: answers.value, questions: questions.value })
    progressAPI.recordActivity({ words_reviewed: questions.value.length, study_minutes: Math.ceil(questions.value.length / 2) }).catch(() => {})
    router.replace(`/quiz/result/${res.data.id}`)
  } catch (e) { console.error('提交失败', e); router.push('/quiz') }
}

onMounted(async () => {
  const count = route.query.count || 10
  const category = route.query.category || ''
  try {
    const res = await quizAPI.generate({ quiz_type: quizType, question_count: parseInt(count), category })
    questions.value = res.data.questions
    if (!questions.value.length) { router.push('/quiz') }
  } catch (e) { console.error('生成题目失败', e); router.push('/quiz') }
  finally { loading.value = false }
})
</script>

<style scoped>
.qt-progress { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
.progress-track { flex: 1; height: 6px; background: var(--bg-hover); border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: var(--accent); border-radius: 3px; transition: width 0.3s; }
.prog-text { font-size: 13px; color: var(--text-muted); white-space: nowrap; }

.qt-question { padding: 32px; max-width: 700px; margin: 0 auto; }
.qt-qnum { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 12px; font-weight: 600; }
.qt-qtext { font-family: var(--font-heading); font-size: 22px; font-weight: 700; margin-bottom: 24px; color: var(--text); }

.qt-options { display: flex; flex-direction: column; gap: 8px; }
.qt-option {
  display: flex; align-items: center; gap: 12px; padding: 14px 18px;
  border: 1.5px solid var(--border); border-radius: var(--radius-sm);
  background: var(--bg-card); font-size: 15px; text-align: left;
  color: var(--text); font-family: var(--font-body); cursor: pointer;
  transition: all var(--transition); width: 100%;
}
.qt-option:hover:not(:disabled) { border-color: var(--accent); }
.qt-option.selected { border-color: var(--accent); background: color-mix(in srgb, var(--accent) 8%, transparent); }
.qt-option.correct { border-color: var(--success); background: color-mix(in srgb, var(--success) 8%, transparent); }
.qt-option.wrong   { border-color: var(--danger); background: color-mix(in srgb, var(--danger) 8%, transparent); }
.qt-option:disabled { opacity: 0.7; cursor: default; }
.opt-letter { width: 28px; height: 28px; border-radius: 50%; background: var(--bg-hover); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; flex-shrink: 0; color: var(--text-secondary); }

.qt-input-area { margin-top: 8px; }
.qt-hint { font-size: 13px; color: var(--text-muted); margin-bottom: 10px; padding: 8px 12px; background: var(--bg-hover); border-radius: var(--radius-sm); }
.qt-input { font-size: 18px; }

.qt-feedback { margin-top: 20px; padding: 16px; border-radius: var(--radius-sm); background: var(--bg-hover); }
.feedback-line { display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 600; }
.feedback-line.correct { color: var(--success); }
.feedback-line.wrong   { color: var(--danger); }
.feedback-answer { margin-top: 8px; font-size: 14px; color: var(--text-secondary); }

.qt-actions { display: flex; gap: 10px; max-width: 700px; margin: 20px auto 0; align-items: center; }
</style>
