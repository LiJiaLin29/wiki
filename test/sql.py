import pytest
from model.models import Ebook, session, Model,Category,EbookDoc
from db.dbInit import engine

@pytest.mark.skip
def test_insert():
    # 插入数据库记录
    # 电子书记录
    i1 = 4
    i2 = i1 + 1
    i3 = i1 + 2
    dicts = [
        {'id':i1,'name': 'Spring Boot入门教程2', 'description':'vvvvv'},
        {'id':i2, 'name': 'Vue入门教程2', 'description':'vvvvv'},
        {'id':i3, 'name': 'Go入门教程2', 'description':'vvvvv'}
    ]
    session.execute(Ebook.__table__.insert(), dicts)
    session.commit()
@pytest.mark.skip
def test_createdb():
    # Model.metadata.drop_all(engine)
    # 创建表
    Model.metadata.create_all(engine)

def test_insert_category():
    # 插入数据库记录
    # 电子书分类记录
    dicts = [
        {'id':1,'parent_id': None,'name': '文档1', 'sort': 1, 'ebook_id': 2},
        {'id':2,'parent_id': 1,'name': '文档1.1', 'sort': 1, 'ebook_id': 2},
        {'id':3,'parent_id': 1,'name': '文档1.2', 'sort': 2, 'ebook_id': 2},
        {'id':4,'parent_id': None,'name': '文档2', 'sort': 2, 'ebook_id': 2},
        {'id':5,'parent_id': 4,'name': '文档2.1', 'sort': 1, 'ebook_id': 2},
        {'id':6,'parent_id': 4,'name': '文档2.2', 'sort': 2, 'ebook_id': 2},
    ]
    session.execute(EbookDoc.__table__.insert(), dicts)
    session.commit()

@pytest.mark.skip
def test_insert_docs():
    # 插入数据库记录
    # 电子书文档记录
    dicts = [
        {'id':100,'parent': 000,'name': '前端开发', 'sort': 100},
        {'id':101,'parent': 100,'name': 'Vue', 'sort': 101},
        {'id':102,'parent': 100,'name': 'Html & CSS', 'sort': 102},
        {'id':200,'parent': 000,'name': 'Java', 'sort': 200},
        {'id':201,'parent': 200,'name': '基础应用', 'sort': 201},
        {'id':202,'parent': 200,'name': '框架应用', 'sort': 202},
        {'id':300,'parent': 000,'name': '数据库', 'sort': 300},
        {'id':301,'parent': 300,'name': 'Mysql', 'sort': 301},
        {'id':302,'parent': 300,'name': 'PostgreSQL', 'sort': 302},
    ]
    session.execute(Category.__table__.insert(), dicts)
    session.commit()