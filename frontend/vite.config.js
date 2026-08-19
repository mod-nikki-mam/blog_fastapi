import { defineConfig } from "vite"
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
  server: {
    origin: "http://127.0.0.1:8000",
    proxy: {
      host: 'localhost',
    },
  },
})
