// nuxt.config.ce.ts
import vuetify from 'vite-plugin-vuetify'

export default defineNuxtConfig({
	compatibilityDate: '2025-07-15',
	ssr: false,

	// Styles nécessaires à Vuetify + icônes MDI
	css: [
		'vuetify/styles',
		'@mdi/font/css/materialdesignicons.css'
	],

	build: {
		transpile: ['vuetify']
	},

	vite: {
		plugins: [
			vuetify({
				autoImport: true,              // tree-shaking auto des comps/directives
				styles: { configFile: false }  // on utilise 'vuetify/styles' (déjà dans css)
			})
		]
	},

	// IMPORTANT : on isole les styles via Shadow DOM
	modules: ['nuxt-custom-elements'],
	customElements: {
		entries: [
			{
				name: 'UiLib',
				shadow: true,
				tags: [
					{
						name: 'VuCard',
						path: '@/components/VuCard.ce.vue'
					}
				]
			}
		]
	},

	// Pas de baseURL/cdnURL ici : les chunks seront résolus relativement au script CE
	app: {
		baseURL: '/',
		cdnURL: '/'
	}
})
