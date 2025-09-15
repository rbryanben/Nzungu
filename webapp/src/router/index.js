import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SalesTab from '@/views/home_tabs/SalesTab.vue'
import InventoryTab from '@/views/home_tabs/InventoryTab.vue'
import AddProductTab from '@/views/home_tabs/AddProductTab.vue'
import ViewSalesTab from '@/views/home_tabs/ViewSalesTab.vue'
import EditProductTab from '@/views/home_tabs/EditProductTab.vue'
import EntryView from '@/views/EntryView.vue'

const routes = [
  {
    path: '/console',
    name: 'console',
    component: HomeView,
    children: [
      {
        path: 'sales',
        name: 'sales',
        component: SalesTab
      },
      {
        path : 'inventory',
        name: 'inventory',
        component: InventoryTab
      },
      {
        path : 'add-product/:reference?',
        name: 'add-product',
        component: AddProductTab
      },
      {
        path : 'edit-product/:reference',
        name: 'edit-product',
        component: EditProductTab
      },
      {
        path: 'view-sales',
        name: 'view-sales',
        component: ViewSalesTab
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/',
    name: 'entry',
    component: EntryView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
