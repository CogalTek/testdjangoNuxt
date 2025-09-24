// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,
	app: {
		// si tu sers à la racine de ton domaine (http://localhost:8000/)
		baseURL: '/'
	}
})
