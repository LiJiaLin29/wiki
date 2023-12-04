import { fileURLToPath, URL } from 'node:url'
import { resolve } from "path"; // 主要用于alias文件路径别名
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default ({command, mode}) => {
  env = loadEnv(mode, process.cwd())
  return defineConfig({
    plugins: [
      vue(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
        'vue': "vue/dist/vue.esm-bundler.js"
      },
      // 导入时想要省略的扩展名列表
      extensions:['.mjs','.js','.ts','.jsx','.tsx','.json'],
    },
    server: {
      // 前端配置
      host: env.VITE_HOST, //ip地址
      port: env.VITE_PORT//端口
    },
    build: {
      // 打包输出
      outDir: env.VITE_APP_NAME
    }
  })

}

