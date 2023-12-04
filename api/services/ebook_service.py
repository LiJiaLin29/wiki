'''
电子书逻辑层代码
'''
from model.models import session, Ebook
from config.logger import myLogger
from typing import List
from schema.schemas import EbookAddRequest, EbookUpdateRequest,EbookSearchRequest
from model.ebook_resp import EbookResponse
from utils.copy_utils import CopyUtils
from model.page import Page
from model.page_resp import PageResponse
from utils.snow_flake import SnowFlake

logger = myLogger(__name__)

class EbookService:

    # 查询电子书列表
    def fetch_all(self, req:EbookSearchRequest):
        result = None
        cond = None
        booklist:List = []
        error = None
        total = None #返回结果数
        # 查询电子书列表
        # 增加按分类查询
        b_name = None
        if req is not None and req.name is not None:
            b_name = req.name.strip()
        # sql表达式
        expr = Ebook.query
        logger.debug(f"DEBUG电子书分类:{req.categoryIds}")
        if req.categoryIds is not None and len(req.categoryIds) > 0:
            logger.debug(f"DEBUG电子书分类:{req.categoryIds}")
            expr = expr.filter(Ebook.category1_id == req.categoryIds[0], Ebook.category2_id == req.categoryIds[1])
        if b_name != '':
            # 大小写不敏感 ilike
            expr = expr.filter(Ebook.name.ilike(f'%{b_name}%'))
        # 获取结果行数，创建分页对象
        total = expr.count()
        try:
            logger.debug(f'current:{req.page}')
            logger.debug(f'total:{total}')
            if req.pageSize is not None:
                page = Page(current=req.page, total=total, pageSize=req.pageSize)
            else:
                page = Page(current=req.page, total=total)
        except Exception as e:
            error = str(e)
            logger.error(f'分页出错：{error}')
            return None, error
        # 增加排序,查询结果不为0，继续执行查询
        if total > 0:
            result = expr.order_by(Ebook.id).limit(page.pageSize()).offset(page.start()).all()
            booklist = CopyUtils.copy_list(result, EbookResponse)
        pageResp = PageResponse(total, booklist)

        logger.debug(f'fetch_all,{booklist}')

        return pageResp, error

    # 更新电子书信息
    def update_ebook(self, req: EbookUpdateRequest):
        error = None
        # 更新记录数
        try:
            # 数据库更新电子书
            # 检查电子书id有效性
            expr = Ebook.query.filter(Ebook.id == req.id)
            num = expr.count()
            if num == 0:
                error = f'电子书id={req.id}无效'
                logger.info(error)
            else:
                # model对象
                ebook = expr.first()
                # 更新对象，obj.字段=值
                CopyUtils.copy_property(req, ebook)
                logger.debug(f'修改电子书数据准备：{ebook.__dict__}')
                # 提交事务
                count = session.commit()
                logger.info(f'成功更新记录')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行电子书更新失败！！"+error)
        return error
    
    # 新增电子书信息
    def add_ebook(self, req: EbookAddRequest):
        error = None
        # 更新记录数
        try:
            # 新增电子书记录，new Ebook数据库对象
            # 雪花算法生成id，赋值电子书id
            ebook = CopyUtils.copy_property_class(req, Ebook)
            ebook.id = SnowFlake(1, 1, 0).get_id()
            logger.debug(f'修改电子书数据准备：{ebook.__dict__}')
            # 数据库插入
            session.add(ebook)
            count = session.commit()
            logger.info(f'成功添加{count}条记录')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行电子书新增失败！！"+error)
        return error

    # 删除电子书信息
    def delete_ebook(self, ids:List):
        error = None
        # 批量删除，或单条记录删除
        try:
            # 删除操作
            logger.debug(f'删除：{ids}')
            Ebook.query.filter(Ebook.id.in_(ids)).delete()
            num = session.commit()
            logger.debug(f'删除条数：{num}')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行电子书删除失败！！"+error)
        return error

    # 根据id查询电子书信息
    def get_by_id(self, id:int):
        error = None
        data = None
        try:
            # 查询操作
            logger.debug(f'查询id：{id}')
            book = Ebook.query.filter(Ebook.id == id).first()
            # id不存在
            if book is None:
                error = f'不存在电子书id={id}!'
            else:
                data = CopyUtils.copy_property_class(book, EbookResponse)
                logger.debug(f'查询结果：{data}')
        except Exception as e:
            error = str(e)
            logger.error(f"数据库执行查询id={id}电子书失败！！{error}")
        return data, error


