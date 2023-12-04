import math
from config.logger import myLogger

logger = myLogger(__name__)
# 分页对象
class Page:

    def __init__(self, total, current, pageSize=5):
        # 初始化：当前页数，总页数，每页数 
        self._pageSize = pageSize if pageSize > 0 else 5
        maxNum = math.ceil(total/pageSize)
        logger.debug(f'最大页码:{maxNum}')
        # 查询结果为空，不判断当前页码
        if total > 0:
            # 页码校验
            if current >= 1 and current <= maxNum:
                self._current = current
            else:
                logger.error('current当前页码无效！！')
                raise Exception('current当前页码无效！！')
            self._start = (self._current-1) * self._pageSize
        self._total = total

        

        

    def start(self):
        # 起始记录数
        return self._start

    def pageSize(self):
        # 每页数
        return self._pageSize