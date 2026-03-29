import {sveltekit} from '@sveltejs/kit/vite'
import tailwindcss from '@tailwindcss/vite'
import {defineConfig} from 'vite'

export default defineConfig({
  build: {
    target: 'es2022',
  },
  plugins: [tailwindcss(), sveltekit()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
