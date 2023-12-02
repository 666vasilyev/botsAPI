<script setup>
import { storeToRefs } from 'pinia'
import { display } from '@/stores/display'
import { DownloadTeamplate } from '@/components'
import { ref } from 'vue'
import { botControl } from '@/stores/botControl'

const storeBot = botControl()
const { getBots } = storeBot

getBots()
  .then(() => {
    isLogin.value = ref(true)

  })
  .catch((err) => {
    console.log(err)
  })

const { getDisplay } = storeToRefs(display())
const isLogin = ref(false)
</script>

<template>
  <DownloadTeamplate v-if="!isLogin" class="download"></DownloadTeamplate>

  <component :is="getDisplay" v-else></component>
</template>

<style lang="scss" scoped>
.download {
  // position: absolute;
  // width: 100vw;
  // height: 100vh;
  // width: 100vw;
  // height: 100vh;
  z-index: 100;
}
</style>
