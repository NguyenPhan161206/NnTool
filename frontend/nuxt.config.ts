export default defineNuxtConfig({
  modules: ["@nuxt/ui"],
  ui: {
    global: true,
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || "http://localhost:8000",
    },
  },
  compatibilityDate: "2025-04-01",
});
