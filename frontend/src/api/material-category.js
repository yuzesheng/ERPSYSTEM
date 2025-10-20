import request from '@/utils/request'

/**
 * 获取物料分类列表
 */
export function getMaterialCategoryList(params) {
  return request({
    url: '/inventory/material-categories/',
    method: 'get',
    params
  })
}

/**
 * 获取物料分类树
 */
export function getMaterialCategoryTree() {
  return request({
    url: '/inventory/material-categories/tree/',
    method: 'get'
  })
}

/**
 * 获取物料分类详情
 */
export function getMaterialCategoryDetail(id) {
  return request({
    url: `/inventory/material-categories/${id}/`,
    method: 'get'
  })
}

/**
 * 创建物料分类
 */
export function createMaterialCategory(data) {
  return request({
    url: '/inventory/material-categories/',
    method: 'post',
    data
  })
}

/**
 * 更新物料分类
 */
export function updateMaterialCategory(id, data) {
  return request({
    url: `/inventory/material-categories/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除物料分类
 */
export function deleteMaterialCategory(id) {
  return request({
    url: `/inventory/material-categories/${id}/`,
    method: 'delete'
  })
}
