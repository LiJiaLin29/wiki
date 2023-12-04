# 包含总条数的返回结果
class PageResponse:
    # 总条数、查询列表
    total:int
    data:list

    def __init__(self, total=None, data=None):
        self.total = total
        self.data = data

    def get_total(self):
        return self.total
    
    def set_total(self, total):
        self.total = total

    def get_data(self):
        return self.data
    
    def set_data(self, data):
        self.data = data


