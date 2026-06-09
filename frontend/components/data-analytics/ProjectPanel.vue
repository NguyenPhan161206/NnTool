<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Projects</h2>
      <UButton size="sm" icon="i-heroicons-plus" @click="showCreate = true">
        New
      </UButton>
    </div>

    <div v-if="showCreate" class="mb-4">
      <UCard>
        <UInput v-model="newName" placeholder="Project name" class="mb-2" />
        <UInput v-model="newDesc" placeholder="Description (optional)" class="mb-2" />
        <div class="flex gap-2">
          <UButton size="sm" :loading="creating" @click="handleCreate">Create</UButton>
          <UButton size="sm" color="gray" @click="cancelCreate">Cancel</UButton>
        </div>
      </UCard>
    </div>

    <div v-if="loading" class="text-center text-gray-400 py-4">Loading...</div>

    <div v-else-if="projects.length === 0" class="text-center text-gray-400 py-4">
      No projects yet. Create one to start.
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="p in projects"
        :key="p.project_id"
        @click="$emit('select', p.project_id)"
        class="p-3 rounded-lg cursor-pointer border transition-colors"
        :class="
          selectedId === p.project_id
            ? 'border-primary bg-primary-50 dark:bg-primary-900/20'
            : 'border-gray-200 dark:border-gray-700 hover:border-primary'
        "
      >
        <div class="font-medium text-sm text-gray-900 dark:text-white">{{ p.name }}</div>
        <div class="text-xs text-gray-500">{{ p.table_count }} table(s)</div>
        <div v-if="p.description" class="text-xs text-gray-400 mt-1 truncate">{{ p.description }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  select: [projectId: string]
  created: []
}>()

defineProps<{
  projects: any[]
  selectedId: string | null
}>()

const api = useApi()
const showCreate = ref(false)
const newName = ref("")
const newDesc = ref("")
const creating = ref(false)
const loading = ref(false)

function cancelCreate() {
  showCreate.value = false
  newName.value = ""
  newDesc.value = ""
}

async function handleCreate() {
  if (!newName.value) return
  creating.value = true
  try {
    await api.createProject(newName.value, newDesc.value)
    cancelCreate()
    emit("created")
  } catch (e: any) {
    console.error(e)
  } finally {
    creating.value = false
  }
}
</script>
