import botAxios from "@/api/botAxios"

export const getBotList = () => {
  return new Promise((res, rej) => {
    botAxios
      .get('/bot/')
      .then((resp) => {
        res(resp?.data)
      })
      .catch((err) => rej(err))
  })
}

export const getBotById = (botId) => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/bot/${botId}`)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const addBot = (params) => {
  const notValid = Object.values(params).includes('')
  if (notValid) throw new Error('addBot have notValid params')

  return new Promise((res, rej) => {
    botAxios
      .post(`/bot/`, params)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const delBotById = (botId) => {
  // const payload = {botId}
  // { data: payload }
  return new Promise((res, rej) => {
    botAxios
      .delete(`/bot/${botId}`)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const updateBotById = (botId) => {
  const payload = {
    alias: 'string',
    description: 'string',
    name: 'string',
    bot_token: 'string',
    channels: ['string'],
    channels_count: 0
  }

  return new Promise((res, rej) => {
    botAxios
      .patch(`/bot/${botId}`, payload)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const getTaskList = () => {
  return new Promise((res, rej) => {
    botAxios
      .get('/task/')
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const getTaskById = (taskId) => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/task/${taskId}`)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const getChannels = () => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/channel/`)
      .then((resp) => res(resp?.data?.all_bundles))
      .catch((err) => rej(err))
  })
}

export const addChannel = (params) => {
  const notValid = Object.values(params).includes('')
  if (notValid) throw new Error('channels have notValid params')

  return new Promise((res, rej) => {
    botAxios
      .post(`/channel/`, params)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const getChannelById = (channelId) => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/channel/${channelId}`)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const delChannelById = (channelId) => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/channel/${channelId}`)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const sendMessage = () => {
  const payload = {
    bot_id: 0,
    channel_id: 'string',
    message: 'string'
  }
  return new Promise((res, rej) => {
    botAxios
      .get(`/message/`, payload)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const login = () => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/login`)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const logout = () => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/logout`)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}

export const statusCheck = ({ botId, channelId }) => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/bot/check_status/${Number(botId)}/${channelId}`)
      .then((resp) => res(resp.data))
      .catch((err) => rej(err))
  })
}

export const postMessageTg = ({ botId, channelId, message }) => {
  const payload = {
    bot_id: botId,
    channel_id: channelId,
    message
  }

  return new Promise((res, rej) => {
    botAxios
      .post(`/message/`, payload)
      .then((resp) => res(resp?.data))
      .catch((err) => rej(err))
  })
}

export const getChannelsActivity = () => {
  return new Promise((res, rej) => {
    botAxios
      .get(`/activity/`)
      .then((resp) => res(resp.data))
      .catch((err) => rej(err))
  })
}

export const updateChannelsActivity = ({channel_id ,activity}) => {
  return new Promise((res, rej) => {
    botAxios
      .post(`/activity/${channel_id}?activity=${activity}`)
      .then((resp) => res(resp))
      .catch((err) => rej(err))
  })
}
