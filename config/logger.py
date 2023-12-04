import logging, yaml
import logging.config
# 实例化logging对象
path = 'logging.yaml'
with open(path,"r") as f:  
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

# 返回具有指定 name 的日志记录器
def myLogger(name):
    logger = logging.getLogger(name)
    return logger