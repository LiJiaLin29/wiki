import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/Main.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: Main
    },
    {
      path: '/admin/ebook',
      name: 'admin-ebook',
      component: () => import('../views/admin/AdminEbook.vue')
    },
    {
      path: '/admin/category',
      name: 'admin-category',
      component: () => import('../views/admin/AdminCategory.vue')
    },
    {
      path: '/admin/docs',
      name: 'admin-ebook-docs',
      // props: true,//允许pros传递路由参数
      component: () => import('../views/admin/AdminEbookDoc.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue')
    }
  ]
})

export default router
