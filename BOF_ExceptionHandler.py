import BOF_ConfigReader
import traceback
import os
import pymysql
import time
import getpass


class ExceptionHandler:
    # 构造函数
    def __init__(self, config):
        self.config = BOF_ConfigReader.ConfigReader(config)
        self.table = 'exceptions'
        self.database_setup()

    # 整理异常信息
    def exc_format(self, err):
        exc_info = traceback.format_exc()
        exc_name = repr(err).split('(')[0]
        line_number = int(exc_info.split('line ')[1].split(',')[0])
        exc_description = repr(err).split('(')[1].strip(')').strip(',').strip("'").strip('"')
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        user = getpass.getuser()

        # 检查用户是否输入文件名 若无则留空缺
        try:
            filename = self.config.get_value('exception_handler', 'filename')
        except:
            filename = None

        return exc_name, current_time, user, filename, line_number, exc_description

    # 把异常信息输入到用户提供的数据库中
    def handle(self, err):
        msg = self.exc_format(err)
        conn = self.setup_connection()
        cursor = conn.cursor()

        insert_values = """INSERT INTO %s""" % self.table + \
                        """(TYPE, TIME, USER, FILENAME, LINE_NUMBER, MESSAGE)
                        VALUES(%s, %s, %s, %s, %s, %s)"""

        insert_without_filename = """INSERT INTO %s""" % self.table + \
                                  """(TYPE, TIME, USER, LINE_NUMBER, MESSAGE)
                                VALUES(%s, %s, %s, %s, %s)"""

        if msg[3] is not None:
            cursor.execute(insert_values, msg)
        else:
            cursor.execute(insert_without_filename, (msg[0], msg[1], msg[2], msg[4], msg[5]))

        conn.commit()

    # 配置数据库表格
    def database_setup(self):
        conn = self.setup_connection()
        cursor = conn.cursor()

        # 若用户提供的表格可用 则采用该表格
        try:
            table = self.config.get_value('exception_handler', 'table')
            cursor.execute('SELECT * FROM %s' % table)
            conn.commit()
            self.table = table

        # 若用户未提供可用表格 创建新表
        except:
            create_table = """CREATE TABLE IF NOT EXISTS exceptions(
                            TYPE VARCHAR(32),
                            TIME VARCHAR(32),
                            USER VARCHAR(32),
                            FILENAME   VARCHAR(255),
                            LINE_NUMBER INT,
                            MESSAGE     VARCHAR(255))"""

            cursor.execute(create_table)
            conn.commit()

    # 建立数据库连接
    def setup_connection(self):
        host = self.config.get_section("exception_handler").get_value('host')
        port = self.config.get_section("exception_handler").get_value('port')
        user = self.config.get_section("exception_handler").get_value('user')
        password = self.config.get_section("exception_handler").get_value('password')
        db = self.config.get_section("exception_handler").get_value('db')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)

        return conn

    # 检查文件是否存在 返回True or False
    @staticmethod
    def check_file(filename):
        file_exists = os.path.exists(filename)
        return file_exists
