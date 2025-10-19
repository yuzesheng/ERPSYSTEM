import Cookies from 'js-cookie'

const TokenKey = import.meta.env.VITE_TOKEN_KEY || 'access_token'
const RefreshTokenKey = import.meta.env.VITE_REFRESH_TOKEN_KEY || 'refresh_token'

// Token管理
export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token, refreshToken) {
  Cookies.set(TokenKey, token)
  if (refreshToken) {
    Cookies.set(RefreshTokenKey, refreshToken)
  }
  return token
}

export function removeToken() {
  Cookies.remove(TokenKey)
  Cookies.remove(RefreshTokenKey)
}

// Refresh Token管理
export function getRefreshToken() {
  return Cookies.get(RefreshTokenKey)
}

export function setRefreshToken(token) {
  return Cookies.set(RefreshTokenKey, token)
}

export function removeRefreshToken() {
  return Cookies.remove(RefreshTokenKey)
}

// 清除所有认证信息
export function clearAuth() {
  removeToken()
  removeRefreshToken()
  localStorage.clear()
  sessionStorage.clear()
}

// 用户信息管理
const UserInfoKey = 'user_info'

export function getUserInfo() {
  const userInfo = localStorage.getItem(UserInfoKey)
  return userInfo ? JSON.parse(userInfo) : null
}

export function setUserInfo(userInfo) {
  return localStorage.setItem(UserInfoKey, JSON.stringify(userInfo))
}

export function removeUserInfo() {
  return localStorage.removeItem(UserInfoKey)
}

// 权限管理
const PermissionsKey = 'user_permissions'

export function getPermissions() {
  const permissions = localStorage.getItem(PermissionsKey)
  return permissions ? JSON.parse(permissions) : []
}

export function setPermissions(permissions) {
  return localStorage.setItem(PermissionsKey, JSON.stringify(permissions))
}

export function removePermissions() {
  return localStorage.removeItem(PermissionsKey)
}

// 检查是否有权限
export function hasPermission(permission) {
  const permissions = getPermissions()
  return permissions.includes(permission) || permissions.includes('*')
}

// 检查是否有任一权限
export function hasAnyPermission(permissionList) {
  const permissions = getPermissions()
  if (permissions.includes('*')) return true
  return permissionList.some(permission => permissions.includes(permission))
}

// 检查是否有所有权限
export function hasAllPermissions(permissionList) {
  const permissions = getPermissions()
  if (permissions.includes('*')) return true
  return permissionList.every(permission => permissions.includes(permission))
}

// 角色管理
const RolesKey = 'user_roles'

export function getRoles() {
  const roles = localStorage.getItem(RolesKey)
  return roles ? JSON.parse(roles) : []
}

export function setRoles(roles) {
  return localStorage.setItem(RolesKey, JSON.stringify(roles))
}

export function removeRoles() {
  return localStorage.removeItem(RolesKey)
}

// 检查是否有角色
export function hasRole(role) {
  const roles = getRoles()
  return roles.includes(role) || roles.includes('admin')
}

// 检查是否有任一角色
export function hasAnyRole(roleList) {
  const roles = getRoles()
  if (roles.includes('admin')) return true
  return roleList.some(role => roles.includes(role))
}

// 菜单管理
const MenusKey = 'user_menus'

export function getMenus() {
  const menus = localStorage.getItem(MenusKey)
  return menus ? JSON.parse(menus) : []
}

export function setMenus(menus) {
  return localStorage.setItem(MenusKey, JSON.stringify(menus))
}

export function removeMenus() {
  return localStorage.removeItem(MenusKey)
}

// 部门管理
const DepartmentKey = 'user_department'

export function getDepartment() {
  const department = localStorage.getItem(DepartmentKey)
  return department ? JSON.parse(department) : null
}

export function setDepartment(department) {
  return localStorage.setItem(DepartmentKey, JSON.stringify(department))
}

export function removeDepartment() {
  return localStorage.removeItem(DepartmentKey)
}

// 检查登录状态
export function isLoggedIn() {
  return !!getToken()
}

// 获取用户ID
export function getUserId() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.id : null
}

// 获取用户名
export function getUsername() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.username : ''
}

// 获取用户姓名
export function getRealName() {
  const userInfo = getUserInfo()
  return userInfo ? userInfo.realName || userInfo.real_name || userInfo.name : ''
}