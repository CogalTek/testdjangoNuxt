// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify from 'vite-plugin-vuetify'

export default defineNuxtConfig({
	compatibilityDate: '2025-07-15',
	devtools: { enabled: true },
	ssr: false,
	app: {
		// si tu sers à la racine de ton domaine (http://localhost:8000/)
		baseURL: '/app_myFrontendNuxtVue_01/',
		cdnURL: '/app_myFrontendNuxtVue_01/',
	},
	css: ['vuetify/styles','@mdi/font/css/materialdesignicons.css'],
	build: { transpile: ['vuetify'] },
	vite: { plugins: [vuetify()] }
})
