import time
import datetime
import BOF_ConfigReader
import pymysql
import getpass
import BOF_ExceptionHandler
time_format = '%Y-%m-%d %H:%M:%S'
timer_user = getpass.getuser()


class Timer:
    # 构造函数
    def __init__(self, config_filename, other=None):
        self.start_time = None
        self.end_time = None
        self.other = other
        self.table = 'timing'
        self.config_filename = config_filename
        self.config = BOF_ConfigReader.ConfigReader(config_filename)
        self.database_setup()

    # 开始计时
    def start_timing(self):
        start_time = time.strftime(time_format, time.localtime(time.time()))
        self.start_time = start_time

    # 终止计时
    def end_timing(self):
        if self.start_time is None:
            return

        try:
            end_time = time.strftime(time_format, time.localtime(time.time()))
            self.end_time = end_time

            param = [timer_user, self.start_time, self.start_time, self.end_time]
            self.database_write(param)
        except Exception as e:
            BOF_ExceptionHandler.ExceptionHandler(self.config_filename).handle(e)

    # 计时结果写入数据库
    def database_write(self, param):
        conn = self.setup_connection()
        cursor = conn.cursor()

        main_keys = ['created_user', 'created_time', 'start_time', 'end_time']
        keys = str(tuple(main_keys)).replace("'", "")
        values = str(tuple(param))

        if self.other is not None:
            keys = str(tuple(main_keys + list(self.other.keys()))).replace("'", "")
            values = str(tuple(param + list(self.other.values())))

        sql_cmd = 'INSERT INTO %s' % self.table + ' %s ' % keys + 'VALUES %s' % values

        cursor.execute(sql_cmd)
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
    def get_start_time(self):
        return self.start_time

    # 获取终止时间
    def get_end_time(self):
        return self.end_time

    # 获取间隔时间
    def get_duration(self):
        start_time = datetime.datetime.strptime(self.start_time, time_format)
        end_time = datetime.datetime.strptime(self.end_time, time_format)
        duration = end_time - start_time
        return str(duration)

    # 重置计时器
    def reset_timer(self):
        self.start_time = None
        self.end_time = None

                                
