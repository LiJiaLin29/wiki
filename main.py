import uvicorn,random, string, time, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #解决跨域问题
from api.routers import hello, ebooks, categorys, ebook_docs # APIRouter 注册的模块
from config.logger import myLogger
from config.app_config import AppConfig
from utils.ip_address import IPAdress

# 获取日志记录对象
logger = myLogger('console')
# fastapi应用
app = FastAPI(title='WIKI API')
# FastAPI app 添加 APIRouter 
app.include_router(hello.router)
app.include_router(ebooks.router)
app.include_router(categorys.router)
app.include_router(ebook_docs.router)

# 项目配置文件读取
config = AppConfig.get_instance()
host = IPAdress.extract_ip()
port = AppConfig.get_port()

# fastapi中间件，【拦截http请求，打印接口耗时日志】，在发送每个请求之前，响应返回之前执行
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"process_time={formatted_process_time}ms \"{request.method} {request.url.path}\" status_code={response.status_code}")
    
    return response
# 支持跨域请求
app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    # expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)



if __name__ == '__main__':
    logger.info("****wiki管理系统启动...")
    # 启用................web服务
    env = None
    logger.info(f'访问地址1：\thttp://{host}:{port}')
    uvicorn.run('main:app', host=host, port=port, reload=True)