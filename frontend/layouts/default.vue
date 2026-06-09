<template>
  <div class="flex h-screen bg-gray-50 dark:bg-gray-900">
    <HubSidebar />
    <main class="flex-1 overflow-auto p-6">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>
