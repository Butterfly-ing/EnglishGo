import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/vocabulary',
    name: 'Vocabulary',
    component: () => import('@/views/Vocabulary.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/vocabulary/:id',
    name: 'WordDetail',
    component: () => import('@/views/WordDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/study/flashcard',
    name: 'FlashCard',
    component: () => import('@/views/FlashCard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: () => import('@/views/Quiz.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/quiz/take/:type',
    name: 'QuizTake',
    component: () => import('@/views/QuizTake.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/quiz/result/:id',
    name: 'QuizResult',
    component: () => import('@/views/QuizResult.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/progress',
    name: 'Progress',
    component: () => import('@/views/Progress.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/articles',
    name: 'Articles',
    component: () => import('@/views/Articles.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/articles/:id',
    name: 'ArticleDetail',
    component: () => import('@/views/ArticleDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    next('/')
  } else {
    next()
  }
})

export default router
