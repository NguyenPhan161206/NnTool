<template>
  <div>
    <h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
      Tool Hub
    </h1>
    <p class="text-gray-600 dark:text-gray-400 mb-6">
      Chon mot tool de bat dau
    </p>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <HubToolCard
        v-for="tool in tools"
        :key="tool.name"
        :tool="tool"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const { data: tools } = useFetch("/api/tools", {
  baseURL: useRuntimeConfig().public.apiBaseUrl,
});
</script>
