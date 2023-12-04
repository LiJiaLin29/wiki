from sqlalchemy.orm import declarative_base,relationship,backref
from sqlalchemy import Column, String, Integer, BigInteger,ForeignKey
from db.dbInit import engine, session

# 定义model与数据库表映射

# 创建model对象的基类
Model = declarative_base()
Model.query = session.query_property()

class Base(Model):
    __abstract__ = True

    # 把SQLAlchemy查询对象转换成字典
    def to_dict(self):
        del self.__dict__['_sa_instance_state']
        return self.__dict__
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 把SQLAlchemy查询对象转换成字典,只包含表字段
    def to_dict_with_col(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Ebook(Base):
    # 电子书表
    __tablename__='ebooks'

    id = Column(BigInteger, primary_key=True, nullable=False, comment='id')
    name = Column(String(50), comment='名称', nullable=True)
    category1_id = Column(BigInteger, comment='分类1')
    category2_id = Column(BigInteger, comment='分类2')
    description = Column(String(200), comment='描述')
    cover = Column(String(200), comment='封面')
    doc_count = Column(Integer, comment='文档数')
    view_count = Column(Integer, comment='阅读数', default=0)
    vote_count = Column(Integer, comment='点赞数', default=0)

    # 一对多
    ebook_docs = relationship('EbookDoc', back_populates='ebook')

    def __repr__(self):
        # 对象的字符串表示
        return f'{self.__class__.__name__},name:{self.name},category1_id:{self.category1_id},\
            category2_id:{self.category2_id}'

class Category(Base):

    __tablename__ = 'categorys'
    id= Column(Integer, primary_key=True, nullable=False, comment='id')
    # 自关联
    parent_id=Column(Integer,ForeignKey('categorys.id'),comment='父级分类')
    name=Column(String(50), nullable=True, comment='分类名称')
    sort=Column(Integer, comment='权重')
    # 自关联关系，关联Model class
    parent = relationship('Category',
        foreign_keys=[parent_id,],
        remote_side=[id],
        backref=backref('childs', lazy='dynamic'))

    def __repr__(self):
        # 对象的字符串表示
        return f'{self.__class__.__name__},name:{self.name},parent:{self.parent_id},\
            sort:{self.sort}'

class EbookDoc(Base):

    __tablename__ = 'ebook_docs'
    id= Column(BigInteger, primary_key=True, nullable=False, comment='id')
    ebook_id=Column(BigInteger,ForeignKey('ebooks.id'),comment='所属电子书id')
    # 自关联
    parent_id=Column(BigInteger,ForeignKey('ebook_docs.id'),comment='父文档')
    name=Column(String(50), nullable=True, comment='文档名称')
    sort=Column(Integer, comment='权重')
    view_count = Column(Integer, comment='阅读数', default=0)
    vote_count = Column(Integer, comment='点赞数', default=0)
    # 自关联关系，关联Model class
    parent = relationship('EbookDoc',
        foreign_keys=[parent_id,],
        remote_side=[id],
        backref=backref('childs', lazy='dynamic'))
    # 一对多
    ebook = relationship('Ebook', back_populates='ebook_docs')

    def __repr__(self):
        # 对象的字符串表示
        return f'{self.__class__.__name__},name:{self.name},ebook_id:{self.ebook_id},parent:{self.parent_id},\
            sort:{self.sort}'


