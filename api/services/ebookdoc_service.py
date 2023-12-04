'''
文档章节树逻辑层代码
'''
from model.models import session, EbookDoc,Ebook
from config.logger import myLogger
from typing import List
from utils.copy_utils import CopyUtils
from utils.model_utils import ModelUtils
from schema.schemas import EbookDocAddRequest, EbookDocUpdateRequest
from sqlalchemy.orm import joinedload
from model.ebook_doc_resp import EbookDocResponse

logger = myLogger(__name__)

class EbookDocService:

    def get_all(self, name:str, ebookId):
        result = []
        error = None
        # 查询文档列表
        try:
            expr = (
                EbookDoc.query
                .options(joinedload(EbookDoc.ebook))
                )
                #     .options(joinedload(User.hobby))
                #     .filter(Hobby.name=='钓鱼')
                #     .all()
            if ebookId is not None:
                expr = expr.filter(EbookDoc.ebook_id == ebookId)
            temp = expr.all()
            
            # 数据库结果转为文档response格式
            for doc in temp:
                logger.debug(f'文档列表：{doc.__dict__}')
                item = CopyUtils[EbookDocResponse].copy_property_class(doc, EbookDocResponse)
                # 电子书名称复制
                item.ebook_name = doc.to_dict()['ebook'].name
                result.append(item)
        except Exception as e:
            error = str(e)
            logger.error("数据库查询文档列表失败！！"+error)
        return result,error

    # 更新文档信息
    def update_ebookdoc(self, req: EbookDocUpdateRequest):
        error = None
        # 更新记录数
        try:
            # 数据库更新文档
            # 检查文档id有效性
            expr = EbookDoc.query.filter(EbookDoc.id == req.id)
            num = expr.count()
            if num == 0:
                error = f'文档id={req.id}无效'
                logger.info(error)
            else:
                # model对象
                ebookdoc = expr.first()
                # 更新对象，obj.字段=值
                CopyUtils.copy_property(req, ebookdoc)
                logger.debug(f'修改文档req：{req}')
                logger.debug(f'修改文档数据准备：{ebookdoc}')
                # 提交事务
                count = session.commit()
                logger.info(f'成功更新记录')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行文档更新失败！！"+error)
        return error
    
    # 新增文档信息
    def add_ebookdoc(self, req: EbookDocAddRequest):
        error = None
        # 新增记录id
        newId = None
        # 更新记录数
        if req is None:
            error = '新增文档内容为空'
            return newId, error
        try:
            # 新增文档记录，new EbookDoc数据库对象
            # 雪花算法生成id，赋值文档id
            ebookdoc = CopyUtils[EbookDoc].copy_property_class(req, EbookDoc)
            logger.debug(f'修改文档数据准备：{EbookDoc.__dict__}')
            # 数据库插入
            session.add(ebookdoc)
            # session.flush()插入新数据推送到数据库，并分配id
            session.flush()
            newId = ebookdoc.id
            session.commit()
            logger.info(f'成功添加文档id:{newId}的记录')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行文档新增失败！！"+error)
        return newId,error

    # 删除文档信息
    def delete_ebookdoc(self, ids:List):
        error = None
        # 批量删除，或单条记录删除
        try:
            # 删除操作, 如果有子文档禁止删除
            logger.debug(f'删除：{ids}')
            count = EbookDoc.query.filter(EbookDoc.parent_id.in_(ids)).count()
            if count>0:
                error='文档下还有子文档，无法删除！'
                logger.debug(error)
            else:
                EbookDoc.query.filter(EbookDoc.id.in_(ids)).delete()
                num = session.commit()
                logger.debug(f'删除条数：{num}')
        except Exception as e:
            error = str(e)
            logger.error("数据库执行文档删除失败！！"+error)
        return error

    # 根据id查询文档信息
    def get_by_id(self, id:int):
        error = None
        resp = None
        try:
            # 查询操作
            logger.debug(f'查询id：{id}')
            ebookdoc = (EbookDoc.query
                    .options(joinedload(EbookDoc.ebook))
                    .filter(EbookDoc.id == id).first()
                    )
            # id不存在
            if ebookdoc is None:
                error = f'不存在文档id={id}!'
            else:
                resp = CopyUtils[EbookDocResponse].copy_property_class(ebookdoc, EbookDocResponse)
                # 电子书名称赋值
                data = ebookdoc.to_dict()
                resp.ebook_name = data['ebook'].name
                logger.debug(f'查询结果：{resp}')
        except Exception as e:
            error = str(e)
            logger.error(f"数据库执行查询id={id}文档失败！！{error}")
        return resp, error
