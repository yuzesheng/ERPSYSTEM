import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getUserInfo as getUserInfoApi, logout as logoutApi } from '@/api/auth'
import { getToken, setToken, removeToken } from '@/utils/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(getToken())
  const userInfo = ref(null)
  const permissions = ref([])
  const roles = ref([])

  // 登录
  const login = async (loginForm) => {
    try {
      const res = await loginApi(loginForm)
      // 后端返回的数据结构: {code: 200, message: '登录成功', data: {access_token, refresh_token, user}}
      const { access_token, refresh_token, user } = res.data
      token.value = access_token
      userInfo.value = user
      setToken(access_token, refresh_token)
      return res
    } catch (error) {
      return Promise.reject(error)
    }
  }

  // 获取用户信息
  const getUserInfo = async () => {
    try {
      const res = await getUserInfoApi()
      userInfo.value = res.data
      permissions.value = res.data.permissions || []
      roles.value = res.data.roles || []
      return res
    } catch (error) {
      return Promise.reject(error)
    }
  }

  // 退出登录
  const logout = async () => {
    try {
      await logoutApi()
    } catch (error) {
      console.error('退出登录失败:', error)
    } finally {
      token.value = ''
      userInfo.value = null
      permissions.value = []
      roles.value = []
      removeToken()
    }
  }

  // 重置token
  const resetToken = () => {
    token.value = ''
    userInfo.value = null
    permissions.value = []
    roles.value = []
    removeToken()
  }

  return {
    token,
    userInfo,
    permissions,
    roles,
    login,
    getUserInfo,
    logout,
    resetToken
  }
})
