<template>
  <el-container class="main-layout">
    <!-- 侧边栏 -->
    <el-aside :width="sidebarWidth" class="sidebar">
      <div class="logo">
        <img src="@/assets/vue.svg" alt="Logo" />
        <span v-if="!appStore.sidebarCollapsed">{{ appTitle }}</span>
      </div>

      <el-menu
        :default-active="activeMenu"
        :collapse="appStore.sidebarCollapsed"
        :unique-opened="true"
        router
      >
        <el-menu-item index="/dashboard">
          <el-icon><Monitor /></el-icon>
          <span>工作台</span>
        </el-menu-item>

        <el-sub-menu index="/foundation">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>基础数据</span>
          </template>
          <el-menu-item index="/foundation/department">
            <el-icon><OfficeBuilding /></el-icon>
            <span>部门管理</span>
          </el-menu-item>
          <el-menu-item index="/foundation/user">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left">
          <el-icon class="toggle-icon" @click="toggleSidebar">
            <Fold v-if="!appStore.sidebarCollapsed" />
            <Expand v-else />
          </el-icon>
        </div>

        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32">{{ userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}</el-avatar>
              <span class="username">{{ userInfo?.username || '用户' }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区域 -->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import {
  Monitor,
  Fold,
  Expand,
  User,
  Setting,
  SwitchButton,
  OfficeBuilding
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

const appTitle = import.meta.env.VITE_APP_TITLE
const userInfo = computed(() => userStore.userInfo)
const activeMenu = computed(() => route.path)
const sidebarWidth = computed(() => appStore.sidebarCollapsed ? '64px' : '200px')

const toggleSidebar = () => {
  appStore.toggleSidebar()
}

const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人中心功能开发中')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中')
      break
    case 'logout':
      ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await userStore.logout()
        ElMessage.success('退出登录成功')
        router.push('/login')
      }).catch(() => {})
      break
  }
}
</script>

<style scoped lang="scss">
.main-layout {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.sidebar {
  background: #304156;
  transition: width 0.3s;

  .logo {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    gap: 10px;

    img {
      width: 32px;
      height: 32px;
    }
  }

  :deep(.el-menu) {
    border: none;
    background: #304156;

    .el-menu-item {
      color: #bfcbd9;

      &:hover {
        background: #263445;
        color: #409eff;
      }

      &.is-active {
        background: #409eff !important;
        color: white;
      }
    }
  }
}

.main-container {
  background: #f0f2f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  padding: 0 20px;

  .header-left {
    .toggle-icon {
      font-size: 24px;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        color: #409eff;
      }
    }
  }

  .header-right {
    .user-info {
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;

      .username {
        font-size: 14px;
      }
    }
  }
}

.main-content {
  padding: 20px;
  overflow-y: auto;
}

// 页面切换动画
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
