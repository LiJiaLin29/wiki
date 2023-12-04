import copy
from typing import List, TypeVar, Generic

# 泛型模板
T = TypeVar('T')
# 复制对象工具类
class CopyUtils(Generic[T]):

    # 单个对象复制
    @staticmethod
    def copy_property_class(from_obj, to_class) -> T:
        'from_obj:原列表数据， to_class:类名 '
        # 对象属性复制
        if from_obj is None:
            raise Exception('from_obj复制对象不能为空')
        obj = to_class()
        for attr, value in vars(from_obj).items():
            if hasattr(obj, attr):
                setattr(obj, attr, value)
        return obj
    
    # 单个对象复制,不生成新的对象
    @staticmethod
    def copy_property(from_obj, to_obj):
        'from_obj:原对象， to_obj:目标对象 '
        # 对象属性复制
        if from_obj is None:
            return None
        for attr, value in vars(from_obj).items():
            if hasattr(to_obj, attr):
                setattr(to_obj, attr, value)
    # 列表对象复制
    @staticmethod
    def copy_list(from_list, to_class) -> List:
        'from_list:原列表数据， to_class:类名 '
        to_list = list()
        # 对象属性复制
        for from_obj in from_list:
            obj = to_class()
            for attr, value in vars(from_obj).items():
                if hasattr(obj, attr):
                    setattr(obj, attr, value)
            to_list.append(obj)
        return to_list