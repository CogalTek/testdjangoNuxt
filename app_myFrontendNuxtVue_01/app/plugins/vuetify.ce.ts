// plugins/vuetify.ce.ts
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
// (optionnel) thèmes et options supplémentaires

export default defineNuxtPlugin((nuxtApp) => {
	const vuetify = createVuetify({
		components,
		directives,
		// theme: { defaultTheme: 'light', themes: { /* ... */ } }
	})
	nuxtApp.vueApp.use(vuetify)
})
