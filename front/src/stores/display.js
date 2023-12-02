import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import {
  BotTest,
  BotPost,
  BotList,
  ChannelList,
  StatsList,
  ChannelStatsList,
  SwaggerApi
} from '@/components'

export const display = defineStore('display', () => {
  const _currDisplay = ref('BotTest')

  const updateDisplay = (newVal) => {
    _currDisplay.value = newVal
  }
  const getDisplay = computed(() => {
    switch (_currDisplay.value) {
      case 'botTest':
        return BotTest
      case 'botPost':
        return BotPost
      case 'botList':
        return BotList
      case 'statsList':
        return StatsList
      case 'chStatsList':
        return ChannelStatsList
      case 'swagger':
        return SwaggerApi
      case 'chanelList':
        return ChannelList
      default:
        return BotTest
    }
  })

  return { getDisplay, updateDisplay }
})
