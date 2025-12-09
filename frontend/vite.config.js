import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080', // Backend URL
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      // Also proxying direct /shifts just in case, though best to prefix requests
      '/shifts': 'http://127.0.0.1:8080',
      '/debug': 'http://127.0.0.1:8080',
    },
  },
})
