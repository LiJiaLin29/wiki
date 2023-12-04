# 字符串常用功能

def is_positive_integer(x):
    # 正整数
    # 判断是否10进制
    if type(x) == str and  not x.isdecimal():
        return False
    x = int(x)
    if isinstance(x, int) and x > 0:
        return True
    return False

t = 'ff022773'
print(is_positive_integer(t))