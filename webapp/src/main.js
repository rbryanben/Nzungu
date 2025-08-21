import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import axios from 'axios'
import { notify_failed } from './utils/notifications'

export const ENDPOINTS = {
    "BASE_URL" : process.env.VUE_APP_BASE_URL,
    "LIVE_UPDATES_ENDPOINT" : process.env.VUE_APP_LIVE_UPDATES_ENDPOINT
}

// Axios inteceptors
axios.interceptors.response.use(
  response => response, 
  error => {
    if (error.response) {
      const { status, data } = error.response;

      if ((status === 401 || status === 403) && data?.action === "AUTH_REQUIRED") {
        router.push({ name: "login" }); 
      }
    }

    return Promise.reject(error);
  }
);

createApp(App).use(store).use(router).mount('#app')
