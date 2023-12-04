'''
电子书分类分类逻辑层代码
'''
from model.models import session, Category
from config.logger import myLogger
from typing import List
from utils.copy_utils import CopyUtils
from utils.model_utils import ModelUtils
from schema.schemas import CategoryAddRequest, CategoryUpdateRequest

logger = myLogger(__name__)

class CategoryService:

    def get_all(self, name:str):
        result = []
        error = None
        # 查询电子书分类列表
        try:
            temp = Category.query.all()
            result = ModelUtils.array2dict(temp)
        except Exception as e:
            error = str(e)
            logger.error("数据库查询分类列表失败！！"+error)
        return result,error

    # 更新电子书分类分类信息
    def update_category(self, req: CategoryUpdateRequest):
        error = None
        # 更新记录数
        try:
            # 数据库更新电子书分类分类
            # 检查电子书分类分类id有效性
            expr = Category.query.filter(Category.id == req.id)
            num = expr.count()
            if num == 0:
                error = f'电子书分类分类id={req.id}无效'
                logger.info(error)
            else:
                # model对象
                category = expr.first()
                # 更新对象，obj.字段=值
                CopyUtils.copy_property(req, category)
                logger.debug(f'修改电子书分类分类req：{req}')
                logger.debug(f'修改电子书分类分类数据准备：{category}')
                # 提交事务
                count = session.commit()
                logger.info(f'成功更新记录')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行电子书分类分类更新失败！！"+error)
        return error
    
    # 新增电子书分类信息
    def add_category(self, req: CategoryAddRequest):
        error = None
        # 新增记录id
        newId = None
        # 更新记录数
        if req is None:
            error = '新增电子书分类内容为空'
            return newId, error
        try:
            # 新增电子书分类记录，new Category数据库对象
            # 雪花算法生成id，赋值电子书分类id
            category = CopyUtils[Category].copy_property_class(req, Category)
            logger.debug(f'修改电子书分类数据准备：{Category.__dict__}')
            # 数据库插入
            session.add(category)
            # session.flush()插入新数据推送到数据库，并分配id
            session.flush()
            newId = category.id
            session.commit()
            logger.info(f'成功添加分类id:{newId}的记录')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行电子书分类新增失败！！"+error)
        return newId,error

    # 删除电子书分类信息
    def delete_category(self, ids:List):
        error = None
        # 批量删除，或单条记录删除
        try:
            # 删除操作, 如果有子分类禁止删除
            logger.debug(f'删除：{ids}')
            count = Category.query.filter(Category.parent_id.in_(ids)).count()
            if count>0:
                error='分类下还有子分类，无法删除！'
                logger.debug(error)
            else:
                Category.query.filter(Category.id.in_(ids)).delete()
                num = session.commit()
                logger.debug(f'删除条数：{num}')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行电子书分类删除失败！！"+error)
        return error

    # 根据id查询电子书分类信息
    def get_by_id(self, id:int):
        error = None
        data = None
        try:
            # 查询操作
            logger.debug(f'查询id：{id}')
            category = Category.query.filter(Category.id == id).first()
            # id不存在
            if category is None:
                error = f'不存在电子书分类id={id}!'
            else:
                data = category.to_dict()
                logger.debug(f'查询结果：{data}')
        except Exception as e:
            error = str(e)
            logger.error(f"数据库执行查询id={id}电子书分类失败！！{error}")
        return data, error
