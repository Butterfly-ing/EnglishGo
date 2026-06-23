import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

// 请求拦截器 - 添加 token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器 - 处理 token 过期
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem('refresh_token')
      if (refresh && !error.config._retry) {
        error.config._retry = true
        try {
          const res = await axios.post('/api/v1/auth/refresh/', { refresh })
          localStorage.setItem('access_token', res.data.access)
          error.config.headers.Authorization = `Bearer ${res.data.access}`
          return api(error.config)
        } catch {
          localStorage.clear()
          router.push('/login')
        }
      }
    }
    return Promise.reject(error)
  }
)

// ===== 用户 API =====
export const authAPI = {
  register(data) { return api.post('/auth/register/', data) },
  login(data) { return api.post('/auth/login/', data) },
  getMe() { return api.get('/auth/me/') },
  refresh(refresh) { return api.post('/auth/refresh/', { refresh }) }
}

// ===== 词汇 API =====
export const vocabularyAPI = {
  getWords(params) { return api.get('/vocabulary/words/', { params }) },
  getWord(id) { return api.get(`/vocabulary/words/${id}/`) },
  createWord(data) { return api.post('/vocabulary/words/', data) },
  updateWord(id, data) { return api.put(`/vocabulary/words/${id}/`, data) },
  deleteWord(id) { return api.delete(`/vocabulary/words/${id}/`) },
  toggleFavorite(id) { return api.post(`/vocabulary/words/${id}/toggle_favorite/`) },
  markMastered(id) { return api.post(`/vocabulary/words/${id}/mark_mastered/`) },
  getFavorites(params) { return api.get('/vocabulary/words/favorites/', { params }) },
  getUnmastered(params) { return api.get('/vocabulary/words/unmastered/', { params }) },
  getCategories() { return api.get('/vocabulary/categories/') }
}

// ===== 测验 API =====
export const quizAPI = {
  generate(data) { return api.post('/quiz/generate/', data) },
  submit(data) { return api.post('/quiz/submit/', data) },
  getHistory() { return api.get('/quiz/history/') },
  getDetail(id) { return api.get(`/quiz/history/${id}/`) }
}

// ===== 进度 API =====
export const progressAPI = {
  getStats() { return api.get('/progress/stats/') },
  getDaily(days = 30) { return api.get('/progress/daily/', { params: { days } }) },
  checkin() { return api.post('/progress/checkin/') },
  recordActivity(data) { return api.post('/progress/record_activity/', data) }
}

// ===== 文章 API =====
export const articleAPI = {
  getList(params) { return api.get('/articles/', { params }) },
  getDetail(id) { return api.get(`/articles/${id}/`) },
  getLevels() { return api.get('/articles/levels/') }
}

export default api
