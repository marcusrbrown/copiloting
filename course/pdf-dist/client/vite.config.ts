import {sveltekit} from '@sveltejs/kit/vite'
import {defineConfig} from 'vite'

export default defineConfig({
  build: {
    target: 'es2022',
  },
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
