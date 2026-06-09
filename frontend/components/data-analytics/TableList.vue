<template>
  <div>
    <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
      Tables ({{ tables.length }})
    </h3>
    <div v-if="tables.length === 0" class="text-xs text-gray-400 italic">
      No tables uploaded yet
    </div>
    <div v-else class="space-y-1">
      <div
        v-for="t in tables"
        :key="t.name"
        class="flex items-center justify-between text-xs bg-gray-50 dark:bg-gray-800 rounded px-2 py-1.5"
      >
        <span class="truncate font-medium">{{ t.name }}</span>
        <span class="text-gray-400 shrink-0 ml-2">{{ t.rows }} rows</span>
        <UButton
          color="red"
          variant="ghost"
          size="2xs"
          icon="i-heroicons-x-mark"
          class="ml-1"
          @click="emit('delete', t.name)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  delete: [tableName: string]
}>()

defineProps<{
  tables: any[]
}>()
</script>
