<template>
	<v-card class="pa-4" elevation="2" max-width="360">
		<v-card-title>{{ title }}</v-card-title>
		<v-card-subtitle v-if="subtitle">{{ subtitle }}</v-card-subtitle>
		<v-card-text>
			<slot />
		</v-card-text>
		<v-card-actions>
			<v-spacer />
			<v-btn variant="text" @click="$emit('primary')">{{ cta || 'OK' }}</v-btn>
		</v-card-actions>
	</v-card>
</template>

<script setup lang="ts">
	defineProps<{
		title?: string
		subtitle?: string
		cta?: string
	}>()
	defineEmits<{ (e: 'primary'): void }>()
</script>
