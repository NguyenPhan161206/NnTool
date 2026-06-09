<template>
  <UCard class="mb-6">
    <h3 class="font-semibold mb-4 text-gray-900 dark:text-white">
      Thong ke du lieu
    </h3>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
        <p class="text-sm text-gray-500">So dong</p>
        <p class="text-xl font-bold">{{ stats.rows }}</p>
      </div>
      <div class="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
        <p class="text-sm text-gray-500">So cot</p>
        <p class="text-xl font-bold">{{ stats.columns }}</p>
      </div>
      <div class="bg-purple-50 dark:bg-purple-900/20 p-3 rounded-lg">
        <p class="text-sm text-gray-500">Missing values</p>
        <p class="text-xl font-bold">{{ totalMissing }}</p>
      </div>
      <div class="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg">
        <p class="text-sm text-gray-500">Cot so</p>
        <p class="text-xl font-bold">{{ numericCols }}</p>
      </div>
    </div>

    <div v-if="stats.numeric_summary && Object.keys(stats.numeric_summary).length">
      <h4 class="font-medium mb-2">Numeric Summary</h4>
      <UTable
        :columns="numericSummaryColumns"
        :rows="numericSummaryRows"
      />
    </div>
  </UCard>
</template>

<script setup lang="ts">
const props = defineProps<{ stats: any }>()

const totalMissing = computed(() => {
  if (!props.stats.missing) return 0
  return Object.values(props.stats.missing).reduce((a: any, b: any) => (a as number) + (b as number), 0)
})

const numericCols = computed(() => {
  if (!props.stats.numeric_summary) return 0
  return Object.keys(props.stats.numeric_summary).length
})

const numericSummaryColumns = computed(() => {
  const cols = Object.keys(props.stats.numeric_summary || {})
  return [
    { key: "stat", label: "Statistic" },
    ...cols.map((c: string) => ({ key: c, label: c })),
  ]
})

const numericSummaryRows = computed(() => {
  const data = props.stats.numeric_summary || {}
  const stats = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
  return stats.map((stat) => {
    const row: any = { stat }
    for (const col of Object.keys(data)) {
      row[col] = data[col]?.[stat] ?? "-"
    }
    return row
  })
})
</script>
