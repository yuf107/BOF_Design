import getpass
import time
import pymysql
import BOF_ConfigReader


class Logger:
    # 构造方法
    def __init__(self, config_filename=None, level='warning'):
        self.user = getpass.getuser()  # 定义user为当前用户登录名
        self.table_name = 'LOGGING'   # 表格名称默认为logging
        self.set_level(level.strip().lower())

        # 若无配置文件，则采取默认设置
        if config_filename is None:
            self.output_is_database = False
            self.filename = None
            return

        # 读取配置文件
        self.config_filename = config_filename
        config = BOF_ConfigReader.ConfigReader(config_filename)

        # 尝试从配置文件中读取输出方式，若无则输出为文本文档
        try:
            self.output_is_database = config.get_value('logger', 'output_is_database')
        except KeyError:
            self.output_is_database = False

        # 尝试从配置文件中读取文件名，若无则空缺
        try:
            self.filename = config.get_value('logger', 'filename')
        except KeyError:
            self.filename = None

        # 若输出为数据库，建立数据库连接
        if self.output_is_database:
            self.database_setup(config_filename)

    # 设置输出级别
    def set_level(self, level):
        if level == 'debug':
            self.level = 0
        elif level == 'info':
            self.level = 1
        elif level == 'warning':
            self.level = 2
        elif level == 'error':
            self.level = 3
        elif level == 'critical':
            self.level = 4

    # debug 级别的运行记录，参数为用户书写的记录信息
    def debug(self, message):
        if self.level > 0:
            return

        if self.output_is_database:
            ls = self.output_format(message)
            ls.insert(0, 'Debug')
            self.write(ls)
            return

        self.write("DEBUG: " + self.output_format(message))

    # info 级别的运行记录，参数为用户书写的记录信息
    def info(self, message):
        if self.level > 1:
            return

        if self.output_is_database:
            ls = self.output_format(message)
            ls.insert(0, 'Info')
            self.write(ls)
            return

        self.write("INFO: " + self.output_format(message))

    # warning 级别的运行记录，参数为用户书写的记录信息
    def warning(self, message):
        if self.level > 2:
            return

        if self.output_is_database:
            ls = self.output_format(message)
            ls.insert(0, 'Warning')
            self.write(ls)
            return

        self.write("WARNING: " + self.output_format(message))

    # error 级别的运行记录，参数为用户书写的记录信息
    def error(self, message):
        if self.level > 3:
            return

        if self.output_is_database:
            ls = self.output_format(message)
            ls.insert(0, 'Error')
            self.write(ls)
            return

        self.write("ERROR: " + self.output_format(message))

    # critical 级别的运行记录，参数为用户书写的记录信息
    def critical(self, message):
        if self.output_is_database:
            ls = self.output_format(message)
            ls.insert(0, 'Critical')
            self.write(ls)
            return

        self.write("CRITICAL: " + self.output_format(message))

    # 整理记录格式：若输出为文本则返回字符串，若为数据库则返回数组
    def output_format(self, message):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg = current_time + ' | ' + self.user + ' | '

        if self.filename is not None:
            msg += self.filename + ' | '

        msg += message + '\n'

        if not self.output_is_database:
            return msg

        return [current_time, self.user, self.filename, message]

    # 输出函数，根据不同输出方式调用不同函数
    def write(self, content):
        if not self.output_is_database:
            Logger.file_write(content)
        else:
            self.database_write(content)

    # 输出到文本文档
    @staticmethod
    def file_write(content):
        filename = 'Logging ' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file = open(filename, 'a')
        file.write(content)
        file.close()

    # 仅供单元测试使用
    @staticmethod
    def file_write_test(content):
        filename = time.strftime('%H-%M-%S', time.localtime(time.time()))
        file = open(filename, 'a')
        file.write(content)
        file.close()

    # 输出到数据库
    def database_write(self, content):
        conn = Logger.setup_connection(self.config_filename)
        cursor = conn.cursor()

        insert_values = """INSERT INTO %s""" % self.table_name + \
                        """(LEVEL, TIME, USER, FILENAME, MESSAGE)
                        VALUES(%s, %s, %s, %s, %s)"""

        cursor.execute(insert_values, (content[0], content[1], content[2], content[3], content[4]))

        conn.commit()

    # 删除数据库表格
    @staticmethod
    def database_reset(config_filename):
        conn = Logger.setup_connection(config_filename)
        cursor = conn.cursor()
        drop_table = """DROP TABLE IF EXISTS LOGGING"""
        cursor.execute(drop_table)

    # 建立数据库表格
    def database_setup(self, config_filename):
        conn = Logger.setup_connection(config_filename)
        cursor = conn.cursor()

        # 若用户已填写表格信息则使用用户创建的表格
        try:
            config_reader = BOF_ConfigReader.ConfigReader(config_filename)
            table = config_reader.get_value('logger', 'table')
            cursor.execute("SELECT * FROM %s" % table)
            self.table_name = table

        # 若无则新建默认表格
        except:
            create_table = """CREATE TABLE IF NOT EXISTS LOGGING(
                                LEVEL  CHAR(8),
                                TIME  CHAR(20),
                                USER  CHAR(16),
                                FILENAME  CHAR(32),
                                MESSAGE  CHAR(80))"""

            cursor.execute(create_table)
            conn.commit()

    # 建立连接
    @staticmethod
    def setup_connection(config_filename):
        config = BOF_ConfigReader.ConfigReader(config_filename)
        host = config.get_section("logger").get_value('host')
        port = config.get_section("logger").get_value('port')
        user = config.get_section("logger").get_value('user')
        password = config.get_section("logger").get_value('password')
        db = config.get_section("logger").get_value('db')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
        return conn

    # 在程序中直接输出数据库的内容
    def database_output(self):
        conn = Logger.setup_connection(self.config_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM %s" % self.table_name)
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        return rows
