import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    // Helps with "access control checks" by ensuring the dev server
    // can access the project root correctly
    fs: {
      allow: ['..'],
    },
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  // This section prevents Vite from trying to process source maps for
  // dependencies that might have broken or inaccessible pointers
  build: {
    sourcemap: false,
  },
  // Specifically ignores source map processing during development
  // for the pre-bundled dependencies seen in your error log
  optimizeDeps: {
    esbuildOptions: {
      sourcemap: false,
    },
  },
})
