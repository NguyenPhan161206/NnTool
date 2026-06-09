<template>
  <div>
    <div
      class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-primary transition-colors"
      @click="openFileDialog"
      @dragover.prevent
      @drop.prevent="handleDrop"
    >
      <UIcon name="i-heroicons-cloud-arrow-up" class="w-12 h-12 mx-auto text-gray-400 mb-4" />
      <p class="text-gray-600 dark:text-gray-400 mb-2">
        Keo tha file CSV vao day hoac click de chon
      </p>
      <p class="text-sm text-gray-400">
        Chi chap nhan file .csv, toi da 50MB
      </p>
    </div>
    <input
      ref="fileInput"
      type="file"
      accept=".csv"
      class="hidden"
      @change="handleFileChange"
    />

    <div v-if="uploadResult" class="mt-4">
      <UCard>
        <p class="font-medium">Da upload: {{ uploadResult.filename }}</p>
        <p class="text-sm text-gray-500">
          {{ uploadResult.rows }} dong, {{ uploadResult.columns.length }} cot
        </p>
        <UTable
          v-if="uploadResult.preview?.length"
          :columns="uploadResult.columns.map((c: string) => ({ key: c, label: c }))"
          :rows="uploadResult.preview"
          class="mt-2"
        />

        <div class="mt-4">
          <UInput
            v-model="question"
            placeholder="Nhap cau hoi cua ban (vd: Doanh thu thang nao cao nhat?)"
            size="lg"
          />
          <UButton
            class="mt-2"
            :loading="analyzing"
            @click="analyzeData"
          >
            Phan tich
          </UButton>
        </div>
      </UCard>
    </div>

    <UAlert v-if="error" type="error" class="mt-4">
      {{ error }}
    </UAlert>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(["uploaded"])
const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl
const fileInput = ref<HTMLInputElement | null>(null)
const question = ref("")
const analyzing = ref(false)
const uploadResult = ref<any>(null)
const error = ref("")

function openFileDialog() {
  fileInput.value?.click()
}

function handleDrop(e: DragEvent) {
  const file = e.dataTransfer?.files[0]
  if (file) uploadFile(file)
}

function handleFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) uploadFile(file)
}

async function uploadFile(file: File) {
  error.value = ""
  if (!file.name.endsWith(".csv")) {
    error.value = "Only .csv files are accepted"
    return
  }
  if (file.size > 50 * 1024 * 1024) {
    error.value = "File too large, max 50MB"
    return
  }

  const formData = new FormData()
  formData.append("file", file)

  try {
    const res = await fetch(`${apiBaseUrl}/api/tools/data-analytics/upload`, {
      method: "POST",
      body: formData,
    })
    if (!res.ok) {
      const err = await res.json()
      error.value = err.detail || "Upload failed"
      return
    }
    uploadResult.value = await res.json()
  } catch (e: any) {
    error.value = "Upload failed: " + e.message
  }
}

async function analyzeData() {
  if (!question.value || !uploadResult.value?.file_id) return
  analyzing.value = true
  error.value = ""

  try {
    const res = await fetch(`${apiBaseUrl}/api/tools/data-analytics/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        file_id: uploadResult.value.file_id,
        question: question.value,
      }),
    })
    if (!res.ok) {
      const err = await res.json()
      error.value = err.detail || "Analysis failed"
      return
    }
    const data = await res.json()
    emit("uploaded", data)
  } catch (e: any) {
    error.value = "Analysis failed: " + e.message
  } finally {
    analyzing.value = false
  }
}
</script>
