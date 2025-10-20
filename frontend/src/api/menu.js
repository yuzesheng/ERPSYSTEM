import request from '@/utils/request'

/**
 * 菜单管理API
 */

// 获取菜单列表
export function getMenuList(params) {
  return request.get('/menus/', params)
}

// 获取菜单树
export function getMenuTree() {
  return request.get('/menus/tree/')
}

// 获取菜单详情
export function getMenuDetail(id) {
  return request.get(`/menus/${id}/`)
}

// 创建菜单
export function createMenu(data) {
  return request.post('/menus/', data)
}

// 更新菜单
export function updateMenu(id, data) {
  return request.put(`/menus/${id}/`, data)
}

// 删除菜单
export function deleteMenu(id) {
  return request.delete(`/menus/${id}/`)
}
