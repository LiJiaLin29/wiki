from pydantic import BaseModel, Field
from typing import Optional

class EbookSearchRequest(BaseModel):
    name:Optional[str] = None
        # 定义默认值
    categoryIds: Optional[list] = None
    page:Optional[int] = Field(default=1)
    pageSize:Optional[int] = Field(default=5)


class EbookAddRequest(BaseModel):
    # 电子书新增
    id: Optional[int] = None
    name: str
    # 默认null
    category1_id: Optional[int] = None
    category2_id: Optional[int] = None
    description: Optional[str]
    cover: Optional[str]
    


class EbookUpdateRequest(BaseModel):
    # 电子书更新
    id: int
    name: str
    # 默认null
    category1_id: Optional[int] = None
    category2_id: Optional[int] = None
    description: Optional[str]
    cover: Optional[str]

    # @validator('id', pre=True)
    # def id_not_null(id):
    #     if id > 5:
    #         raise ValueError('电子书id不能为空！')
    #     return id

class CategoryAddRequest(BaseModel):
    # 电子书分类新增
    id: Optional[int] = None
    name: str
    parent_id: Optional[int] = None
    sort: Optional[int] = Field(default=0)

    # @validator('id', pre=True)
    # def id_is_num(id):
    #     if not is_positive_integer(id):
    #         raise ValueError('分类编号只能输入数字！')
    #     id = int(id)
    #     return id



class CategoryUpdateRequest(BaseModel):
    # 电子书分类更新
    id: Optional[int]
    name: str
    parent_id: Optional[int] = None
    sort: Optional[int] = Field(default=0)

class EbookDocAddRequest(BaseModel):
    # 文档新增
    id: Optional[int] = None
    ebook_id: int
    name: str
    parent_id: Optional[int] = None
    sort: Optional[int] = Field(default=0)

class EbookDocUpdateRequest(BaseModel):
    # 文档更新
    id: Optional[int] = None
    ebook_id: int
    name: str
    parent_id: Optional[int] = None
    sort: Optional[int] = Field(default=0)
    # 默认值
    view_count:Optional[int] = Field(default=0)
    vote_count:Optional[int] = Field(default=0)
