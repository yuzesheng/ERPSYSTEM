import request from '@/utils/request'

/**
 * 部门管理API
 */

// 获取部门列表
export function getDepartmentList(params) {
  return request.get('/departments/', params)
}

// 获取部门树
export function getDepartmentTree() {
  return request.get('/departments/tree/')
}

// 获取部门详情
export function getDepartmentDetail(id) {
  return request.get(`/departments/${id}/`)
}

// 创建部门
export function createDepartment(data) {
  return request.post('/departments/', data)
}

// 更新部门
export function updateDepartment(id, data) {
  return request.put(`/departments/${id}/`, data)
}

// 删除部门
export function deleteDepartment(id) {
  return request.delete(`/departments/${id}/`)
}
