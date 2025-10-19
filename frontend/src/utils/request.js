import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'
import { getToken, removeToken } from '@/utils/auth'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_USE_PROXY ? '/api' : import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 添加token
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }

    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }

    return config
  },
  error => {
    console.error('请求错误：', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data

    // 如果是下载文件，直接返回
    if (response.config.responseType === 'blob') {
      return response
    }

    // 根据自定义的错误码进行判断
    if (res.code !== 200 && res.code !== 0) {
      ElMessage({
        message: res.message || '请求失败',
        type: 'error',
        duration: 5000
      })

      // 401: Token过期或未登录
      if (res.code === 401) {
        ElMessageBox.confirm(
          '登录状态已过期，请重新登录',
          '系统提示',
          {
            confirmButtonText: '重新登录',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          const userStore = useUserStore()
          userStore.logout().then(() => {
            router.push('/login')
          })
        })
      }

      // 403: 没有权限
      if (res.code === 403) {
        ElMessage({
          message: '您没有权限访问该资源',
          type: 'error',
          duration: 5000
        })
      }

      return Promise.reject(new Error(res.message || '请求失败'))
    } else {
      // 返回完整的响应对象,保持data字段
      return res
    }
  },
  error => {
    console.error('响应错误：', error)

    let message = '请求失败'

    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求参数错误'
          break
        case 401:
          message = '未授权，请重新登录'
          const userStore = useUserStore()
          userStore.logout().then(() => {
            router.push('/login')
          })
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求地址不存在'
          break
        case 408:
          message = '请求超时'
          break
        case 500:
          message = '服务器内部错误'
          break
        case 501:
          message = '服务未实现'
          break
        case 502:
          message = '网关错误'
          break
        case 503:
          message = '服务不可用'
          break
        case 504:
          message = '网关超时'
          break
        case 505:
          message = 'HTTP版本不受支持'
          break
        default:
          message = `连接错误${error.response.status}`
      }
    } else if (error.message.includes('timeout')) {
      message = '请求超时'
    } else if (error.message.includes('Network')) {
      message = '网络错误，请检查您的网络连接'
    }

    ElMessage({
      message,
      type: 'error',
      duration: 5000
    })

    return Promise.reject(error)
  }
)

// 导出请求方法
export default service

// 封装常用请求方法
export const request = {
  get(url, params = {}, config = {}) {
    return service({
      url,
      method: 'get',
      params,
      ...config
    })
  },

  post(url, data = {}, config = {}) {
    return service({
      url,
      method: 'post',
      data,
      ...config
    })
  },

  put(url, data = {}, config = {}) {
    return service({
      url,
      method: 'put',
      data,
      ...config
    })
  },

  patch(url, data = {}, config = {}) {
    return service({
      url,
      method: 'patch',
      data,
      ...config
    })
  },

  delete(url, params = {}, config = {}) {
    return service({
      url,
      method: 'delete',
      params,
      ...config
    })
  },

  // 上传文件
  upload(url, file, data = {}, config = {}) {
    const formData = new FormData()
    formData.append('file', file)

    // 添加其他数据
    Object.keys(data).forEach(key => {
      formData.append(key, data[key])
    })

    return service({
      url,
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      ...config
    })
  },

  // 下载文件
  download(url, params = {}, filename = 'download', config = {}) {
    return service({
      url,
      method: 'get',
      params,
      responseType: 'blob',
      ...config
    }).then(response => {
      const blob = new Blob([response.data])
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = filename
      link.click()
      window.URL.revokeObjectURL(link.href)
    })
  }
}