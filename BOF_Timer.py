import time
import datetime
import BOF_ConfigReader
import pymysql


class Timer:
    # 构造函数
    def __init__(self, config_filename=""):
        self.times = {}
        self.format = '%Y-%m-%d %H:%M:%S'
        self.config = None

        if config_filename == "":
            return

        self.table = 'timing'
        self.config = BOF_ConfigReader.ConfigReader(config_filename)
        self.database_setup()

    # 开始计时
    def start_timing(self, name, number=-1):  # 若用户未填写ID 默认填入-1
        key = name + str(number)
        start_time = time.strftime(self.format, time.localtime(time.time()))
        self.times[key] = [name, number, start_time]

    # 终止计时
    def end_timing(self, name, number=-1):
        key = name + str(number)
        end_time = time.strftime(self.format, time.localtime(time.time()))
        self.times[key].append(end_time)

        if self.config is not None:
            t = self.times[key]
            param = (t[0], t[1], t[2], t[3], self.get_duration(name, number))

            self.database_write(param)

    # 计时结果写入数据库
    def database_write(self, param):
        conn = self.setup_connection()
        cursor = conn.cursor()

        insert_values = """INSERT INTO %s""" % self.table + \
                        """(NAME, ID, START, END, DURATION)
                        VALUES(%s, %s, %s, %s, %s)"""

        cursor.execute(insert_values, param)
        conn.commit()

    # 配置数据库表格
    def database_setup(self):
        conn = self.setup_connection()
        cursor = conn.cursor()

        # 若用户提供的表格可用 则采用该表格
        try:
            table = self.config.get_value('timer', 'table')
            cursor.execute('SELECT * FROM %s' % table)
            conn.commit()
            self.table = table

        # 若用户未提供可用表格 创建新表
        except:
            create_table = """CREATE TABLE IF NOT EXISTS TIMING(
                            NAME CHAR(32),
                            ID   INT,
                            START CHAR(32),
                            END   CHAR(32),
                            DURATION  CHAR(16))"""
            cursor.execute(create_table)
            conn.commit()

    # 建立数据库连接
    def setup_connection(self):
        host = self.config.get_section("timer").get_value('host')
        port = self.config.get_section("timer").get_value('port')
        user = self.config.get_section("timer").get_value('user')
        password = self.config.get_section("timer").get_value('password')
        db = self.config.get_section("timer").get_value('db')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)

        return conn

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
