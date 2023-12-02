<template>
  <div class="download">
    <circle-download class="download__circle" />
  </div>
</template>

<script setup>
import CircleDownload from '@/components/CircleDownload.vue';
</script>

<style lang="scss" scoped>
.download {
  position: relative;

  width: 100%;
  height: 100%;
  background: #0000003b;
  display: flex;
  justify-content: center;

  // .download__circle
  &__circle {
    width: 25%;
    height: 25%;
  }
}
</style>
