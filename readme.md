wiki知识库系统

python技术栈
前端：
- vue框架
- vue UI组件库： ant design vue
后端：
- python + fastapi + uvicorn python异步服务器
- 包环境：wiki
  激活环境：activate wiki
  退出环境：deactivate
- 日志配置：
- main.py项目入口文件
- 环境配置文件:
- 前端：.env.dev|.env.prod
        vite.config.js vite配置文件,配置服务启动端口等
- 后端：resources/application.propertites
项目启动：
后端：python -m main
前端：  
      cd ./web 进入web前端源代码目录
      npm run serve:dev 开发环境
