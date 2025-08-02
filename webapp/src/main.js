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

// Response Interceptor
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        notify_failed('Authorization failed - Please login again')
      } 
      else if (error.response.status === 500) {
        notify_failed('Server Error')
      }
    } else if (error.request) {
      notify_failed('Network error - Check your internet connection.');
    } 

    return Promise.reject(error);
  }
);

createApp(App).use(store).use(router).mount('#app')
