<template>
    <a-layout style="min-height: 480px;">
      <!-- 分类侧边栏 -->
        <a-layout-sider width="200" style="background: #fff">
          <a-menu
            v-model:selectedKeys="selectedKeys2"
            v-model:openKeys="openKeys"
            mode="inline"
            :style="{ height: '100%', borderRight: 0 }"
            @click="tabSideMenu"
          >
          <a-menu-item key="welcome">
            <template #icon>
              <HomeOutlined />
            </template>
            欢迎
          </a-menu-item>
          <template v-for="item in list" :key="item.id">
            <template v-if="!item.childs">
              <a-menu-item :key="item.id">
                <template #icon>
                  <PieChartOutlined />
                </template>
                {{ item.name }}
              </a-menu-item>
            </template>
            <template v-else>
              <sub-menu :menu-info="item" :key="item.id" />
            </template>
          </template>
          </a-menu>
        </a-layout-sider>
        <a-layout style="padding: 0 24px 24px">
          <!-- 当前分类 -->
          <a-breadcrumb style="margin-top: 16px;">{{ currentPath.join('/') }}</a-breadcrumb>
          <a-layout-content
            :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
          >
          <div v-show="isShowWelcome"><h2>欢迎页~~</h2></div>
          <!-- 电子书列表 -->
          <a-list v-show="!isShowWelcome" :grid="{ gutter: 8, column: 3 }" :pagination="pagination" :data-source="ebooks">
            <template #renderItem="{ item }">
              <a-list-item key="item">
                <!-- 电子书描述信息 -->
                <a-list-item-meta :description="item.description">
                  <!-- 名称 -->
                  <template #title>
                    <a :href="item.href" class="book-title">{{ item.name }}</a>
                  </template>
                  <!-- 封面图片 -->
                  <template #avatar>
                    <a-avatar shape="square" size="large" :src="item.cover" />
                  </template>
                </a-list-item-meta>
                <!-- content 操作图标 -->
                <div style="margin-left: 56px;display:grid;grid-template-columns: 33.33% 33.33% 33.33%;">
                  <span v-for="{ icon, text } in actions" :key="icon">
                      <component :is="icon" style="margin-right: 8px" />
                      {{ text }}
                  </span>
                </div>
              </a-list-item>
            </template>
          </a-list>
          </a-layout-content>
        </a-layout>
        
      </a-layout>
</template>
<script lang="ts">
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { StarOutlined, UserOutlined, HeartOutlined,PieChartOutlined,HomeOutlined } from '@ant-design/icons-vue';
import { tools } from '@/assets/js/tools'
import qs from 'qs'

const pagination = {
  onChange: (page: number) => {
    console.log(page);
  },
  pageSize: 3,
};
// 图标
const actions: Record <string,any> [] = [
  { icon: StarOutlined },
  { icon: UserOutlined },
  { icon: HeartOutlined },
];
//自定义子菜单
const SubMenu = {
  name: 'SubMenu',
  props: {
    menuInfo: {
      type: Object,
      default: () => ({}),
    },
  },
  template: `
    <a-sub-menu :key="menuInfo.id">
      <template #title>{{ menuInfo.name }}</template>
      <template v-for="item in menuInfo.childs" :key="item.id">
        <template v-if="!item.childs">
          <a-menu-item :key="item.id">
            {{ item.name }}
          </a-menu-item>
        </template>
        <template v-else>
          <sub-menu :menu-info="item" :key="item.id" />
        </template>
      </template>
    </a-sub-menu>
  `,
};

export default{
  setup(){
    //定义变量
    
    const ebookUrl = '/v1/ebooks'
    const categoryUrl = '/v1/categorys'
    const selectedKeys1 = ref<string[]>(['2']);
    const selectedKeys2 = ref<string[]>(['1']);
    const openKeys = ref<string[]>(['sub1']);
    const ebooks = ref()//响应式对象
    const categorys=[]
    // 侧边分类菜单
    const list = ref([])
    //当前路径
    const currentPath=ref([])
    //页面内容切换
    let isShowWelcome = ref(true)

    // 生命周期钩子
    onMounted(
      ()=>{
        // 查询电子书列表
        fetchEbookList(null)
        // 查询分类列表
        axios.get(categoryUrl).then((response) => {
          const data = response.data.content
          list.value = tools.array2tree(data, null)

          // 遍历，获取分类数组
            for(let i in data){
              const v = data[i]
              categorys[v.id] = v.name
            }
            console.log('categorys', categorys[100]);
        })
      }
    )
    const fetchEbookList=function(params){
      axios.get(ebookUrl,{params:params,
                          paramsSerializer: params => {
                            return qs.stringify(params, { indices: false })
                          }})
                          .then((response) => {
          const data = response.data
          ebooks.value = data.content.data
      })
    }
      // 点击侧边菜单，查询对应分类电子书
    const tabSideMenu = (e: Event) => {
      
      // 判断是否点击欢迎页
      const current = e.key
      if(current==='welcome'){
        isShowWelcome.value = true
      }else{// 点击分类,非欢迎页
        isShowWelcome.value = false
        // 修改当前分类,清空分类信息
        currentPath.value.splice(0, currentPath.value.length)
        for(let i in e.keyPath){
          const v = e.keyPath[i]
          console.log('点击分类内容', v);
          currentPath.value.push(categorys[v])
        }
        // 查询电子书列表
        console.log('click', e);
        console.log('currentPath', currentPath.value);
        const params = {
          'categoryIds': e.keyPath
        }
        fetchEbookList(params)
      }
      
    };
    return {
      isShowWelcome,
      ebooks,
      selectedKeys2,
      openKeys,
      pagination,
      actions,
      list,//分类菜单
      tabSideMenu,
      currentPath//当前分类
    }
  },
  components: {
    'sub-menu': SubMenu,//自定义子菜单
    HomeOutlined
  },
}
</script>

<style scoped>
  .site-layout-background {
    background: #fff;
  }
  .book-title{
    font-size: 20px;
    font-weight: bold;
  }
</style>