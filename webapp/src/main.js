import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'

export const ENDPOINTS = {
    "BASE_URL" : "http://localhost:8000"
}

createApp(App).use(store).use(router).mount('#app')
