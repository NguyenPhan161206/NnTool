<template>
  <div class="flex gap-6 h-full">
    <div class="w-72 shrink-0">
      <UCard class="sticky top-6">
        <DataAnalyticsProjectPanel
          :projects="projects"
          :selected-id="activeProjectId"
          @select="selectProject"
          @created="loadProjects"
        />
        <UDivider class="my-4" />
        <DataAnalyticsTableList
          v-if="activeProject"
          :tables="activeProject.tables"
          @delete="handleDeleteTable"
        />
      </UCard>
    </div>

    <div class="flex-1 min-w-0">
      <template v-if="!activeProjectId">
        <UCard>
          <h2 class="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
            Data Analytics
          </h2>
          <p class="text-gray-600 dark:text-gray-400">
            Select or create a project from the left panel to start analyzing multi-table data.
          </p>
        </UCard>
      </template>

      <template v-else>
        <DataAnalyticsMultiFileUpload
          :project-id="activeProjectId"
          @uploaded="refreshProject"
        />

        <div class="mt-4">
          <UCard>
            <UInput
              v-model="question"
              placeholder="Ask a question across all tables..."
              size="lg"
            />
            <UButton
              class="mt-3"
              :loading="analyzing"
              :disabled="!question"
              @click="analyzeProject"
            >
              {{ analyzing ? 'Analyzing...' : 'Analyze Project' }}
            </UButton>
          </UCard>
        </div>

        <div v-if="report" class="mt-4">
          <DataAnalyticsLLMReport :content="report" />
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
const api = useApi()

const projects = ref<any[]>([])
const activeProjectId = ref<string | null>(null)
const activeProject = ref<any>(null)
const question = ref("")
const analyzing = ref(false)
const report = ref("")
const abortController = ref<AbortController | null>(null)

async function loadProjects() {
  try {
    projects.value = await api.listProjects()
  } catch (e) {
    console.error(e)
  }
}

async function selectProject(id: string) {
  activeProjectId.value = id
  report.value = ""
  question.value = ""
  await refreshProject()
}

async function refreshProject() {
  if (!activeProjectId.value) return
  try {
    activeProject.value = await api.getProject(activeProjectId.value)
  } catch (e) {
    console.error(e)
  }
}

async function handleDeleteTable(tableName: string) {
  if (!activeProjectId.value) return
  try {
    await api.deleteTable(activeProjectId.value, tableName)
    await refreshProject()
  } catch (e: any) {
    console.error(e)
  }
}

async function analyzeProject() {
  if (!activeProjectId.value || !question.value) return
  analyzing.value = true
  report.value = ""

  abortController.value = new AbortController()
  const timeout = setTimeout(() => abortController.value?.abort(), 600000)

  try {
    const data = await api.analyzeProject(activeProjectId.value, question.value, abortController.value.signal)
    report.value = data.report
  } catch (e: any) {
    if (e.name === "AbortError") {
      report.value = "Request timed out. Try a simpler question."
    } else {
      report.value = "Error: " + e.message
    }
  } finally {
    clearTimeout(timeout)
    analyzing.value = false
    abortController.value = null
  }
}

loadProjects()
</script>
