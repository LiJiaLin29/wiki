<template>
    <a-layout-header class="header">
        <div class="logo" />
        <a-menu
          :selectedKeys="[$route.name]"
          theme="dark"
          mode="horizontal"
          :style="{ lineHeight: '64px' }"
        >
          <a-menu-item v-for="m in menuList" :key="m.herf">
            <RouterLink :to="{ name: m.herf }" >{{m.name}}
            </RouterLink>
        </a-menu-item>
        </a-menu>
      </a-layout-header>
</template>
<script>
import { RouterLink } from 'vue-router';

export default{
    data() {
        return {
            'menuList': null,
        };
    },
    mounted() {
        // 渲染组件
        this.menuList = [
            { id: 1, name: '首页', herf: 'main' , path: '/'},
            { id: 2, name: '电子书管理' , herf: 'admin-ebook', path: '/admin/ebook'},
            { id: 3, name: '分类管理' , herf: 'admin-category', path: '/admin/category'},
            { id: 4, name: '关于' , herf: 'about', path: '/about'}
        ];
    },
    components: { RouterLink }
}
</script>