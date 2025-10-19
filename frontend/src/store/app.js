import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 侧边栏是否折叠
  const sidebarCollapsed = ref(false)

  // 切换侧边栏
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // 设备类型
  const device = ref('desktop') // desktop | mobile

  // 设置设备类型
  const setDevice = (type) => {
    device.value = type
  }

  return {
    sidebarCollapsed,
    toggleSidebar,
    device,
    setDevice
  }
})
