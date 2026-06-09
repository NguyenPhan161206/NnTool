<template>
  <aside class="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4 flex flex-col">
    <NuxtLink to="/" class="text-lg font-bold mb-6 text-primary">
      Tool Hub
    </NuxtLink>
    <nav class="space-y-1 flex-1">
      <NuxtLink
        v-for="tool in tools"
        :key="tool.name"
        :to="`/tools/${tool.name}`"
        class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
      >
        <UIcon :name="tool.icon || 'i-heroicons-cube'" class="w-4 h-4" />
        {{ tool.description || tool.name }}
      </NuxtLink>
    </nav>
  </aside>
</template>

<script setup lang="ts">
const { data: tools } = useFetch("/api/tools", {
  baseURL: useRuntimeConfig().public.apiBaseUrl,
  server: false,
});
</script>
