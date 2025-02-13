import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/HomePage.vue') }]
  },
  {
    path: '/users/:id',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', name: 'UserPage', component: () => import('pages/UserPage.vue') }]
  },
  {
    path: '/:catchAll(.*)*',
    name: 'NotFound',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
