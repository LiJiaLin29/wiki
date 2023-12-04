'''
数据库model对象常用方法
'''
from typing import List
from model.models import Base

class ModelUtils:

    @staticmethod
    def array2dict(array:List[Base]) -> List:
        result = []
        # 遍历model列表，转为字典对象
        for item in array:
            t = item.to_dict()
            result.append(t)
        return result
