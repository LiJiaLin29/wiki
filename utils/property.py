# property文件处理工具
class Properties:

    def __init__(self, file_name):
        self.file_name = file_name
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r', encoding='utf-8')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        else:
            fopen.close()

    def contains_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if self.contains_key(key):
            return self.properties[key]
        return default_value
    
    def parse(file_name):
        # 读取文件
        return Properties(file_name)