<script setup>
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { DefaultLayout, AuthLayout } from "@/layout";

const route = useRoute();
const layout = computed(() => {
  switch (route.meta.layout) {
    case 'default':
      return DefaultLayout;
    default:
      return AuthLayout;
  }
})
</script>

<template>
  <component :is="layout">
    <RouterView />
  </component>
</template>

<style scoped>
</style>
