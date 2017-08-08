import logging
import time
import codecs


# 定义一个类别名为Section 最终的输出为数个section组成的数组
class Section:
    # 初始化方法 定义变量name为分区名称 变量actual为一个储存实际内容的字典
    def __init__(self, name):
        self.name = name
        self.actual = {}

    # 在分区中写入新的特征名称和值
    def write(self, key, value):
        self.actual[key] = value

    # 在分区中按照特征名称获取特征值
    def get_value(self, key):
        try:
            return self.actual[key]
        except KeyError:
            return None


# 定义名为ConfigReader的类别 其中的变量content包含一个配置文件中所有的内容
class ConfigReader:
    def __init__(self, filename):
        file = codecs.open(filename, 'rb')
        self.content = ConfigReader.read(file)
        file.close()

    # 获取配置文件的某个分区
    def get_section(self, name):
        for section in self.content:
            if section.name == name:
                return section

    # 获取分区中某个特征值
    def get_value(self, section_name, key_name):
        return self.get_section(section_name).get_value(key_name)

    # 读取整个文件
    @staticmethod
    def read(file):
        sections = []  # 由所有分区组成的数组, 包含配置文件的所有内容

        line_count = 0  # 统计行数
        for line in file.read().decode('utf-8').split('\n'):  # 添加对中文字符的支持
            line_count += 1

            # 处理注释
            if line.strip().startswith('#'):
                continue

            # 处理空白行
            if line.strip() == "":
                continue

            # 读取分区名称并添加到sections数组
            if line.strip().startswith('['):
                section_name = line[line.find('[') + 1: line.find(']')]
                sections.append(Section(section_name))

                logging_message = "[New section created: " + section_name + " ]"
                logging.info(logging_message)

                continue

            # 找到等号的位置
            key_and_value = line.split(' = ', 1)

            # 忽略没有等号的语句
            if len(key_and_value) == 1:
                logging_message = "[ Unrecognized sentence at line No. " + str(line_count) + ' ]'
                logging.warning(logging_message)
                continue

            # 把特征值从字符串改变为需要的类型
            value = ConfigReader.read_all(key_and_value[1])

            logging_message = "[ Appending key value:  " + key_and_value[0] + " : " \
                              + str(value).strip('\n') + " ]"
            logging.info(logging_message)
            sections[len(sections) - 1].write(key_and_value[0], value)

        return sections

    @staticmethod
    # 读取日期和时间
    def read_datetime(string):
        # 读取时间
        try:
            t = time.strptime(string, "%H:%M:%S")
            log_msg = "[Time " + string + " is transferred from string to time.]"
            logging.info(log_msg)
            return t
        except ValueError:
            logging.debug("Not a time")

        # 读取日期和时间
        try:
            t = time.strptime(string, "%Y-%m-%d %H:%M:%S")
            log_msg = "[Datetime " + string + " is transferred from string to datetime.]"
            logging.info(log_msg)
            return t
        except ValueError:
            logging.debug("Not a datetime")

        # 读取日期
        try:
            t = time.strptime(string, "%Y-%m-%d")
            log_msg = "[Date " + string + " is transferred from string to date.]"
            logging.info(log_msg)
            return t
        except ValueError:
            logging.debug("Not a date.")

        # 若不是以上任一种类 则返还字符串本身
        return string

    @staticmethod
    # 读取一个数组
    def read_list(string):
        output_list = []
        string = string.strip()
        string = string[1:]  # 去掉开头的[

        working = ""  # 添加到数组中的元素

        index = 0
        while index < len(string):
            char = string[index]  # 循环字符串的每个字符
            index += 1

            # 遇见逗号 尝试转换元素类别 添加元素到数组并继续循环
            if char == ",":
                output_list.append(ConfigReader.read_all(working))
                working = ""
                continue

            # 遇见后方括号 尝试转换元素类别 添加元素到数组并跳出循环
            if char == "]":
                output_list.append(ConfigReader.read_all(working))
                break

            # 读取引号中的字符串
            if char == '"':
                result = ConfigReader.read_quotation(string[index - 1:])
                output_list.append(result[0])

                # 把正在读取的字符位置调到最近的逗号或中括号后面
                index += result[1]
                while string[index] != "," and string[index] != "]":
                    index += 1
                index += 1

                continue

            working = working + char  # 在暂存元素的字符串中添加当前字符

        return output_list

    @staticmethod
    # 读取数组和字典中的引号
    def read_quotation(string):
        string = string.strip()[1:]  # 忽略字符串开头的引号
        output_string = ""

        # 逐个字符循环 遇到后引号后跳出
        index = 0
        while index in range(len(string)):
            char = string[index]

            if char == '"':
                break

            output_string += char
            index += 1

        return output_string, index

    @staticmethod
    # 读取字典
    def read_dict(string):
        output_dict = {}
        string = string.strip()
        string = string[1:]  # 去掉字符串开头的{

        working = ""  # 暂存当前元素名称或值的内容
        key = ""  # 当前元素的名称
        index = 0
        while index < len(string):
            char = string[index]
            index += 1  # 循环字符串中的每个字符

            # 读取字典元素的名称
            if char == ":":
                key = working.strip()

                # 字典元素名称转为字符串或整数
                if key.strip().startswith('"') and key.strip().endswith('"'):
                    key = key.strip()[1:len(key.strip()) - 1]
                else:
                    try:
                        key = int(key)
                    except ValueError:
                        logging.debug("Not an int")

                working = ""  # 清空暂存的 字符串
                continue

            # 读取字典元素值中的引号
            if char == '"':
                in_quotation = ConfigReader.read_quotation(string[index - 1:])

                if in_quotation[0] != "":
                    output_dict[key] = ConfigReader.read_datetime(in_quotation[0])

                index += in_quotation[1] + 1
                continue

            # 读取字典元素的值 并转化为相应的格式
            if char == ",":
                working = ConfigReader.read_all(working)

                if working != "":  # 检验暂存的字符串是否为空 防止覆盖已写入的元素
                    output_dict[key] = working

                working = ""
                continue

            # 同样读取元素值 读取后 跳出循环
            if char == '}':
                working = ConfigReader.read_all(working)

                if working != "":
                    output_dict[key] = working

                break

            # 读取字典中的数组
            if char == "[":
                output_dict[key] = ConfigReader.read_list(string[index - 1:])
                key = "to_delete"  # 读取数组后 标记当前元素为待删除
                continue

            # 读取字典中的字典
            if char == "{":
                (output_dict[key], dict_length) = ConfigReader.read_dict(string[index - 1:])
                index += dict_length  # 读取字典后 更新当前字符在字符串的位置
                continue

            working = working + char

        # 尝试删除标记为待删除的元素
        try:
            del output_dict["to_delete"]
        except KeyError:
            logging.debug("")

        return output_dict, index

    # 读取各个种类的特征值
    @staticmethod
    def read_all(string):
        string = string.strip()

        # 读取带引号的字符串
        if string.strip().startswith('"') and string.strip().endswith('"'):
            string = string.strip()[1:len(string.strip()) - 1]
            return string

        # 读取dictionary
        if string.startswith('{') and string.endswith('}'):
            return ConfigReader.read_dict(string)[0]

        # 读取list
        if string.startswith('[') and string.endswith(']'):
            return ConfigReader.read_list(string)

        # 读取boolean
        if string.lower() == "true":
            return True
        if string.lower() == "false":
            return False

        # 读取整数
        try:
            return int(string)
        except ValueError:
            logging.debug("Not an int")

        # 读取浮点数
        try:
            return float(string)
        except ValueError:
            logging.debug("Not a float")

        # 读取时间和日期 若都不是则返回字符串本身
        return ConfigReader.read_datetime(string)

    # 显示配置文件的内容
    def write(self):
        for section in self.content:
            print(section.name)

            for key in section.actual:
                print(key, section.actual[key])

            print()
