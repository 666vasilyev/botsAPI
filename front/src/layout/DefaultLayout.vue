<template>
  <div class="layout">
    <nav-menu class="nav-menu"> </nav-menu>

    <router-view class="main-area"></router-view>
  </div>
</template>

<script setup>
import { NavMenu } from '@/components'
import { RouterView } from 'vue-router'
</script>

<style lang="scss" scoped>
.layout {
  display: flex;
  width: 100%;
  height: 100%;

  .nav-menu {
    flex-basis: 35%;
    max-width: 500px;
    padding: 2% 2% 0;
    background: #1c273d;
  }

  .main-area {
    width: 100%;
    height: 100%;
    padding: 5% 5% 2%;
  }
}
</style>
