import request from '@/utils/request'

/**
 * 角色管理API
 */

// 获取角色列表
export function getRoleList(params) {
  return request.get('/roles/', params)
}

// 获取角色详情
export function getRoleDetail(id) {
  return request.get(`/roles/${id}/`)
}

// 创建角色
export function createRole(data) {
  return request.post('/roles/', data)
}

// 更新角色
export function updateRole(id, data) {
  return request.put(`/roles/${id}/`, data)
}

// 删除角色
export function deleteRole(id) {
  return request.delete(`/roles/${id}/`)
}

// 获取权限列表
export function getPermissionList(params) {
  return request.get('/permissions/', params)
}
