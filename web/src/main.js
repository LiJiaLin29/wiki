import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue'
import { message } from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import axios from 'axios'
import store from './store/index'


const app = createApp(App)

// AntdUI组件 全局注册
app.use(router).use(Antd).use(store)
// axios配置全局 ,将全局模块挂载到vue组件上,使用this.Common.变量
app.config.globalProperties.$ajax = axios 
// app.config.globalProperties.Common = Common
// app.provide('COMMON', COMMON)
axios.defaults.baseURL=import.meta.env.VITE_API_URL;
//axios拦截器，打印前端日志
//请求拦截器
axios.interceptors.request.use(
    config =>{
    // 打印请求信息
    console.log(`请求参数： ${config.url}: `, config.data, config.params);
    return config;
    },
    error =>{
    return Promise.reject(error);
    }
);
//响应拦截器
axios.interceptors.response.use(
    response =>{
    // 打印后端返回的结果
    console.log(`返回结果： ${response.config.url}: `, response.data);
    // 操作成功提示
    if(!response.data.success){
        message.error(response.data.message)
    }
    return response;
    },
    error =>{
    let msg = JSON.stringify(error.response.data)
    if (error.response.status == 504||error.response.status == 404) {
          message.error('服务器被吃了⊙﹏⊙∥'+msg)
      } else if (error.response.status == 403) {
        message.error('权限不足,请联系管理员!'+msg)
      }else {
        message.error('未知错误!'+msg)
      }
      console.log(error.response);
      return Promise.resolve(error);
    },
);


app.mount('#app')

// console.log(import.meta.env.VITE_API_URL)
// console.log(import.meta.env.VITE_ENV)
