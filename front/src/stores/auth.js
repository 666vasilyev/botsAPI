import { defineStore } from 'pinia'
import { login as log, logout as lgout } from '@/api/auth'
import router from '@/router'
// import botAxios from "@/api/botAxios"

export const auth = defineStore('auth-store', () => {
  const login = (params) => {
    log(params)
      .then(() => {
        router.push({ name: 'home' })
      })
      .catch((err) => {
        console.log('err login', err)
      })
  }

  const logout = () => {
    return lgout()
  }

  const register = () => {}

  return {
    login,
    logout,
    register
  }
})
