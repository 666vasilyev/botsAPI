import authAxios from "@/api/authAxios"

export const login = ({username, password}) => {
    return new Promise((res, rej) => {
        authAxios
        .post(`/auth/jwt/login`, `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`)
        .then((resp) => res(resp))
        .catch((err) => rej(err))
    })
  }

  export const logout = () => {
  
    return new Promise((res, rej) => {
        authAxios
        .post(`/auth/jwt/logout`)
        .then((resp) => res(resp))
        .catch((err) => rej(err))
    })
  }

  export const register = (botId) => {
    const payload = {
      alias: 'string',
      description: 'string',
      name: 'string',
      bot_token: 'string',
      channels: ['string'],
      channels_count: 0
    }
  
    return new Promise((res, rej) => {
        authAxios
        .patch(`/bot/${botId}`, payload)
        .then((resp) => res(resp))
        .catch((err) => rej(err))
    })
  }
