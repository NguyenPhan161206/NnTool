<template>
  <UCard class="mb-6">
    <h3 class="font-semibold mb-4 text-gray-900 dark:text-white">
      Bao cao AI
    </h3>
    <div class="prose dark:prose-invert max-w-none">
      {{ content }}
    </div>
  </UCard>
</template>

<script setup lang="ts">
defineProps<{ content: string }>()
</script>
