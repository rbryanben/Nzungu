import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SalesTab from '@/views/home_tabs/SalesTab.vue'
import InventoryTab from '@/views/home_tabs/InventoryTab.vue'
import AddProductTab from '@/views/home_tabs/AddProductTab.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    children: [
      {
        path: '/',
        name: 'sales',
        component: SalesTab
      },
      {
        path : 'inventory',
        name: 'inventory',
        component: InventoryTab
      },
      {
        path : 'add-product',
        name: 'add-product',
        component: AddProductTab
      },
      {
        path : 'edit-product/:reference',
        name: 'edit-product',
        component: SalesTab
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
