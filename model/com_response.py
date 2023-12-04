'''
自定义接口返回类
'''
from enum import Enum
from objtyping import to_primitive

class MsgEnum(str,Enum):
    # 操作信息
    SUCCESS = '操作成功'
    ERROR = '操作失败'


class ComResponse:


    def __init__(self):
        self.success = True
        self.message = MsgEnum.SUCCESS
        self.content = None


    def set_success(self, success):
        self.success = success

    def set_message(self, message):
        self.message = message

    def set_content(self, content):
        self.content = content

    def get_success(self):
        return self.success

    def get_message(self):
        return self.message

    def get_content(self):
        return self.content