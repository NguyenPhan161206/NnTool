<template>
  <NuxtLink :to="`/tools/${tool.name}`">
    <UCard class="hover:shadow-lg transition-shadow cursor-pointer">
      <div class="flex items-center gap-3">
        <UIcon :name="tool.icon || 'i-heroicons-cube'" class="w-8 h-8 text-primary" />
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white">
            {{ tool.description || tool.name }}
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ tool.name }}
          </p>
        </div>
      </div>
    </UCard>
  </NuxtLink>
</template>

<script setup lang="ts">
defineProps<{ tool: { name: string; description?: string; icon?: string } }>()
</script>
