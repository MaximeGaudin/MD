import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import {createRouter, createWebHistory,} from 'vue-router/auto'
import {setupLayouts} from 'virtual:generated-layouts'

const router = createRouter({
    history: createWebHistory(),
    extendRoutes: (routes) => setupLayouts(routes)
})

createApp(App)
    .use(router)
    .mount('#app')
