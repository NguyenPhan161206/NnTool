<template>
  <UCard class="mb-6">
    <h3 class="font-semibold mb-4 text-gray-900 dark:text-white">
      Bieu do
    </h3>
    <div v-for="(chart, i) in charts" :key="i" class="mb-4">
      <VChart
        v-if="chartOptions(chart)"
        :option="chartOptions(chart)"
        autoresize
        class="h-80 w-full"
      />
    </div>
  </UCard>
</template>

<script setup lang="ts">
import VChart from "vue-echarts"
import { use } from "echarts/core"
import { CanvasRenderer } from "echarts/renderers"
import { LineChart, BarChart, ScatterChart } from "echarts/charts"
import { GridComponent, TooltipComponent, LegendComponent } from "echarts/components"

use([CanvasRenderer, LineChart, BarChart, ScatterChart, GridComponent, TooltipComponent, LegendComponent])

const props = defineProps<{ charts: any[] }>()

function chartOptions(chart: any) {
  if (!chart?.data) return null
  const data = chart.data
  if (!data?.data) return null

  const traces = Array.isArray(data.data) ? data.data : [data.data]

  const series = traces.map((trace: any) => ({
    name: trace.name || "",
    type: chart.chart_type === "bar" ? "bar" : chart.chart_type === "line" ? "line" : "bar",
    data: Array.isArray(trace.y) ? trace.y : [],
    smooth: chart.chart_type === "line",
  }))

  const xData = traces[0]?.x || []

  return {
    tooltip: { trigger: "axis" },
    legend: { data: series.map((s: any) => s.name) },
    grid: { left: 60, right: 20, bottom: 40, top: 40 },
    xAxis: { type: "category", data: xData },
    yAxis: { type: "value" },
    series,
  }
}
</script>
