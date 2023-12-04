import time
from datetime import datetime

"""
雪花算法生成全局自增唯一id
存储组成：符号位+时间戳13位+工作机器ID（机房+机器号）最多10位+序列号12位
16位id接口返回才正确，不然fastapi总是会四色五入？？
"""

# 64位ID的划分
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 3
SEQUENCE_BITS = 10

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter元年时间戳1288834974657
TWEPOCH = 1672502400000 # 2023年1月1号


class SnowFlake(object):
    """
    用于生成IDs
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 其实序号
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            logger.error('clock is moving backwards. Rejecting requests until{}'.format(self.last_timestamp))
            raise Exception

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | (
                    self.worker_id << WOKER_ID_SHIFT) | self.sequence

        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


__worker = SnowFlake(1, 1, 0)

def generate_id():
    return __worker.get_id()


if __name__ == '__main__':
    # 起始时间戳
    # 将指定日期字符串转换为日期对象
    # date_obj = datetime.strptime('2023-01-01', "%Y-%m-%d")
    # # 将日期对象转换为时间戳
    # timestamp = int(date_obj.timestamp() * 1000)
    # print(timestamp)
    for i in range(10):
            id = generate_id()
            print(id)