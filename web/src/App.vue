<template>
    <a-layout>
      <!-- 传递选中菜单id参数， 通过props选项接收 -->
      <TheHeader />
      <RouterView />
      <TheFooter />
    </a-layout>
  </template>
<!-- <script lang="ts" setup> -->
<script lang="ts">
import TheHeader from './components/TheHeader.vue';
import TheFooter from './components/TheFooter.vue';

export default{
  components:{
    TheHeader,
    TheFooter
  }
}
</script>
  <style scoped>
  #components-layout-demo-top-side-2 .logo {
    float: left;
    width: 120px;
    height: 31px;
    margin: 16px 24px 16px 0;
    background: rgba(255, 255, 255, 0.3);
  }
  
  .ant-row-rtl #components-layout-demo-top-side-2 .logo {
    float: right;
    margin: 16px 0 16px 24px;
  }
  </style>