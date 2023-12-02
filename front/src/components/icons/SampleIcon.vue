<template>
  <div v-html="svg"></div>
</template>

<script setup>
import { computed, toRefs } from "vue";

const props = defineProps({
  name: {
    type: String,
    default: "home",
  },
});

const { name } = toRefs(props);

const modules = import.meta.glob("./**/*.svg", {
  as: "raw",
  eager: true,
});

const svg = computed(() => {
  return modules["./icon-" + name.value + ".svg"] ?? modules["./home.svg"];
});
</script>
