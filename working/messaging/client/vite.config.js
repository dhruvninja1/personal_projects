import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key: fs.readFileSync('../key/192.168.1.172+1-key.pem'),
      cert: fs.readFileSync('../key/192.168.1.172+1.pem'),
    },
    port: 5173, // Vite's default port
  },
})