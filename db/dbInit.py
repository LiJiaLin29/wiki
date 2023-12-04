from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config.app_config import AppConfig
from config.logger import myLogger

# 获取日志记录对象
logger = myLogger('console')

# 获取数据库配置信息
config = AppConfig.get_instance()
host = config.get('database.host')
name=config.get('database.name')
user=config.get('database.user')
password=config.get('database.password')
poolSize=config.get('database.poolSize')
timeout=config.get('database.timeout')
driver=config.get('database.driver')

# postgreSQL
engine = create_engine(
    # postgresql://myusername:mypassword@localhost:5432/mydatabase
    url=f'{driver}://{user}:{password}@{host}/{name}', #数据库地址
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=int(poolSize),  # 连接池大小
    pool_timeout=int(timeout),  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    echo=True, # 打印sql语句
    client_encoding='utf8'
)
# 创建session对象
session = scoped_session(sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
))

# 插入单条数据
def insert_one(one):
    session.add(one)
    session.commit()

# 批量插入记录
def insert_objects(objects):
    session.bulk_save_objects(objects)
    session.commit()

# 查询表记录
def select_where(table, where_clause=None):
    resList = None
    if where_clause is None:
        resList = session.query(table).all()
    else:
        print(where_clause)
        resList = session.query(table).filter_by(where_clause).all()
    return resList

# 查询表记录
def select(table, **kwargs):
    sql = [a for k in kwargs.keys]
    resList = session.query(table).filter_by(where_clause)
    return resList