import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getBotList,
  addBot,
  addChannel,
  getChannels,
  statusCheck,
  postMessageTg as postTg,
  getChannelsActivity as getChAct,
  updateChannelsActivity as updChannelsActivity
} from '@/api/apiRequest'

export const botControl = defineStore('bot-control', () => {
  const botList = ref([])

  const getBotsId = computed(() =>
    botList.value.map((el) => {
      const { id, name } = el
      return { id, name }
    })
  )
  const getBots = async () => {
    return new Promise((res, rej) => {
      getBotList()
        .then((result) => {
          result.map((el) => (el['created_at'] = el['created_at'].split('T')[0]))
          botList.value = result
          res("SUCCESS")
        })
        .catch(() => {
          rej("ERROR")
        })
    })
    // return getBotList()
    //   .then((result) => {
    //     console.log('botList.value', result)
    //     result.map((el) => (el['created_at'] = el['created_at'].split('T')[0]))
    //     botList.value = result
    //   })
    //   .catch((err) => {
    //     console.log(err)
    //   })
  }

  const createBot = ({ alias, description, name, botToken }) => {
    const reqParams = {
      alias,
      description,
      name,
      bot_token: botToken
    }

    return addBot(reqParams)
  }
  // channels block
  const channels = ref([])
  const getChanels = () => {
    getChannels()
      .then((result) => {
        result.map((el) => (el['created_at'] = el['created_at'].split('T')[0]))
        channels.value = result
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const createChanel = ({ channel, bot_id }) => {
    const params = {
      channel,
      bot_id
    }
    return addChannel(params)
  }

  const statCheck = async ({ botId, channelId }) => {
    return statusCheck({ botId, channelId })
  }

  const postMessageTg = (params) => {
    return postTg(params)
  }

  const channelsState = ref([])
  const getChannelsActivity = () => {
    return getChAct()
      .then((result) => {
        channelsState.value = result.all_activity
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const updateChannelsActivity = (params) => {
    return updChannelsActivity(params)
  }
  return {
    botList,
    getBots,
    createBot,
    getBotsId,
    createChanel,
    channels,
    getChanels,
    statCheck,
    postMessageTg,
    updateChannelsActivity,
    getChannelsActivity,
    channelsState
  }
})
