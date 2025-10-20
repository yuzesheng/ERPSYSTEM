import request from '@/utils/request'

/**
 * 获取物料列表
 */
export function getMaterialList(params) {
  return request({
    url: '/inventory/materials/',
    method: 'get',
    params
  })
}

/**
 * 获取物料详情
 */
export function getMaterialDetail(id) {
  return request({
    url: `/inventory/materials/${id}/`,
    method: 'get'
  })
}

/**
 * 创建物料
 */
export function createMaterial(data) {
  return request({
    url: '/inventory/materials/',
    method: 'post',
    data
  })
}

/**
 * 更新物料
 */
export function updateMaterial(id, data) {
  return request({
    url: `/inventory/materials/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除物料
 */
export function deleteMaterial(id) {
  return request({
    url: `/inventory/materials/${id}/`,
    method: 'delete'
  })
}
