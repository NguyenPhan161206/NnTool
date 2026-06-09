<template>
  <div>
    <UCard>
      <div
        class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center cursor-pointer hover:border-primary transition-colors"
        @click="openFileDialog"
        @dragover.prevent
        @drop.prevent="handleDrop"
      >
        <UIcon name="i-heroicons-cloud-arrow-up" class="w-10 h-10 mx-auto text-gray-400 mb-3" />
        <p class="text-gray-600 dark:text-gray-400">Upload CSV files to project</p>
        <p class="text-sm text-gray-400">.csv only, max 50MB each</p>
      </div>
      <input
        ref="fileInput"
        type="file"
        multiple
        accept=".csv"
        class="hidden"
        @change="handleFileChange"
      />
    </UCard>

    <div v-if="uploading.length > 0" class="mt-3 space-y-2">
      <div
        v-for="item in uploading"
        :key="item.name"
        class="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-800 rounded px-3 py-2"
      >
        <span>{{ item.name }}</span>
        <span v-if="item.done" class="text-green-600">Done</span>
        <span v-else-if="item.error" class="text-red-600">{{ item.error }}</span>
        <span v-else class="text-blue-600">Uploading...</span>
      </div>
    </div>

    <UAlert v-if="error" type="error" class="mt-3">{{ error }}</UAlert>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  projectId: string
}>()

const emit = defineEmits<{
  uploaded: []
}>()

const api = useApi()
const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref<any[]>([])
const error = ref("")

function openFileDialog() {
  fileInput.value?.click()
}

function handleDrop(e: DragEvent) {
  const files = Array.from(e.dataTransfer?.files || [])
  files.forEach((f) => uploadFile(f))
}

function handleFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  const files = Array.from(target.files || [])
  files.forEach((f) => uploadFile(f))
  target.value = ""
}

async function uploadFile(file: File) {
  error.value = ""
  if (!file.name.endsWith(".csv")) {
    error.value = `${file.name} is not a .csv file`
    return
  }
  if (file.size > 50 * 1024 * 1024) {
    error.value = `${file.name} exceeds 50MB`
    return
  }

  const entry = { name: file.name, done: false, error: "" }
  uploading.value.push(entry)

  try {
    await api.uploadToProject(props.projectId, file)
    entry.done = true
    emit("uploaded")
  } catch (e: any) {
    entry.error = e.message
  }
}
</script>
