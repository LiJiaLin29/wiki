from utils.property import Properties
from config.logger import myLogger
import os

# 获取日志记录对象
logger = myLogger('console')

# 处理项目配置文件
class AppConfig:
    # 配置文件对象，单例
    __config = None

    @classmethod #类方法
    def get_instance(cls):
        #当__instance为空时，创建对象
        if not cls.__config:
            # 创建配置文件对象
            cls.__config=cls.server_cofig()
        return cls.__config

    @classmethod
    def server_cofig(cls, env=None) -> Properties:
        prop = None
        path = f'resources/application.propertites'
        # 处理服务器配置文件
        if env is not None:
            path = f'resources/application-{env}.propertites'
        try:
            logger.info(f'配置文件路径：{path}')
            if os.path.isfile(path):
                prop = Properties.parse(path)
            else:
                raise FileNotFoundError(f'{path}配置文件不存在')
        except FileNotFoundError as e:
            logger.exception('项目配置文件不存在！')
        # logger.info('prop:', prop)
        return prop

    @classmethod
    def get_port(cls):
        port = 8000
        if cls.__config is not None and cls.__config.contains_key('server.port'):
            t_port = cls.__config.get('server.port')
            logger.debug(f't_port: {t_port}')
            if t_port.isnumeric:
                port = int(t_port)
        return port