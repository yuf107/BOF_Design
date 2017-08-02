import time
import datetime


class Timer:
    # 构造函数
    def __init__(self):
        self.times = {}
        self.format = '%Y-%m-%d %H:%M:%S'

    # 开始计时
    def start_timing(self, name, number=-1):
        key = name + str(number)
        start_time = time.strftime(self.format, time.localtime(time.time()))
        self.times[key] = [name, number, start_time]

    # 终止计时
    def end_timing(self, name, number=-1):
        key = name + str(number)
        end_time = time.strftime(self.format, time.localtime(time.time()))
        self.times[key].append(end_time)

    # 获取开始时间
    def get_start_time(self, name, number=-1):
        key = name + str(number)
        return self.times[key][2]

    # 获取终止时间
    def get_end_time(self, name, number=-1):
        key = name + str(number)
        return self.times[key][3]

    # 获取间隔时间
    def get_duration(self, name, number=-1):
        key = name + str(number)
        start_time = datetime.datetime.strptime(self.times[key][2], self.format)
        end_time = datetime.datetime.strptime(self.times[key][3], self.format)
        duration = end_time - start_time
        return str(duration)

    def get_times(self, name, number=-1):
        key = name + str(number)
        return self.times[key]
