import request from '@/utils/request'

/**
 * 用户登录
 * @param {Object} data - 登录信息 { username, password }
 */
export const login = (data) => {
  return request.post('/auth/login/', data)
}

/**
 * 用户退出登录
 */
export const logout = () => {
  return request.post('/auth/logout/')
}

/**
 * 获取用户信息
 */
export const getUserInfo = () => {
  return request.get('/auth/userinfo/')
}

/**
 * 刷新Token
 * @param {String} refresh - Refresh Token
 */
export const refreshToken = (refresh) => {
  return request.post('/auth/token/refresh/', { refresh })
}

/**
 * 修改密码
 * @param {Object} data - { old_password, new_password }
 */
export const changePassword = (data) => {
  return request.post('/auth/change-password/', data)
}

/**
 * 重置密码
 * @param {Object} data - { email }
 */
export const resetPassword = (data) => {
  return request.post('/auth/reset-password/', data)
}
