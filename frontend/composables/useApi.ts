export const useApi = () => {
  const apiBaseUrl = useRuntimeConfig().public.apiBaseUrl

  const BASE = `${apiBaseUrl}/api/tools/data-analytics`

  async function upload(file: File) {
    const formData = new FormData()
    formData.append("file", file)
    const res = await fetch(`${BASE}/upload`, {
      method: "POST",
      body: formData,
    })
    if (!res.ok) throw new Error((await res.json()).detail || "Upload failed")
    return res.json()
  }

  async function analyze(fileId: string, question: string) {
    const res = await fetch(`${BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file_id: fileId, question }),
    })
    if (!res.ok) throw new Error((await res.json()).detail || "Analysis failed")
    return res.json()
  }

  async function createProject(name: string, description: string) {
    const res = await fetch(`${BASE}/project/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description }),
    })
    if (!res.ok) throw new Error((await res.json()).detail || "Create project failed")
    return res.json()
  }

  async function listProjects() {
    const res = await fetch(`${BASE}/projects`)
    if (!res.ok) throw new Error("Failed to list projects")
    return res.json()
  }

  async function getProject(projectId: string) {
    const res = await fetch(`${BASE}/project/${projectId}`)
    if (!res.ok) throw new Error("Project not found")
    return res.json()
  }

  async function deleteProject(projectId: string) {
    const res = await fetch(`${BASE}/project/${projectId}`, { method: "DELETE" })
    if (!res.ok) throw new Error("Delete failed")
    return res.json()
  }

  async function uploadToProject(projectId: string, file: File) {
    const formData = new FormData()
    formData.append("file", file)
    const res = await fetch(`${BASE}/project/${projectId}/upload`, {
      method: "POST",
      body: formData,
    })
    if (!res.ok) throw new Error((await res.json()).detail || "Upload failed")
    return res.json()
  }

  async function analyzeProject(projectId: string, question: string, signal?: AbortSignal) {
    const res = await fetch(`${BASE}/project/${projectId}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
      signal,
    })
    if (!res.ok) throw new Error((await res.json()).detail || "Analysis failed")
    return res.json()
  }

  async function deleteTable(projectId: string, tableName: string) {
    const res = await fetch(`${BASE}/project/${projectId}/table/${encodeURIComponent(tableName)}`, { method: "DELETE" })
    if (!res.ok) throw new Error((await res.json()).detail || "Delete failed")
    return res.json()
  }

  return {
    upload,
    analyze,
    createProject,
    listProjects,
    getProject,
    deleteProject,
    uploadToProject,
    analyzeProject,
    deleteTable,
  }
}
