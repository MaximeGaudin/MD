import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import VueRouter from 'unplugin-vue-router/vite'
import Layouts from 'vite-plugin-vue-layouts';

// https://vitejs.dev/config/
export default defineConfig({
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:8090',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''),
            },
        }
    },
    plugins: [
        VueRouter({
            routesFolder: [
                {
                    src: 'src/pages'
                }
            ]
        }),
        Layouts({
            layoutsDirs: 'src/layouts'
        }),

        // Must be last
        vue()
    ],
})
