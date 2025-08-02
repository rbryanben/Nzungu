import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import axios from 'axios'
import { notify_failed } from './utils/notifications'

export const ENDPOINTS = {
    "BASE_URL" : "http://127.0.0.1:8000"
}

createApp(App).use(store).use(router).mount('#app')
