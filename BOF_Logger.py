import getpass
import time
import pymysql
import BOF_ConfigReader


class Logger:
    def __init__(self, database_config=None, user="", filename=""):
        if user == "":
            self.user = getpass.getuser()
        else:
            self.user = user

        self.filename = filename

        if database_config is None:
            self.output_is_database = False
        else:
            self.output_is_database = True
            self.config_filename = database_config
            Logger.database_setup(database_config)

    def debug(self, message):
        if self.output_is_database:
            self.write(self.output_format(message).insert(0, 'Debug'))
            return

        self.write("DEBUG: " + self.output_format(message))

    def info(self, message):
        if self.output_is_database:
            self.write(self.output_format(message).insert(0, 'Info'))
            return

        self.write("INFO: " + self.output_format(message))

    def warning(self, message):
        if self.output_is_database:
            self.write(self.output_format(message).insert(0, 'Warning'))
            return

        self.write("WARNING: " + self.output_format(message))

    def error(self, message):
        if self.output_is_database:
            ls = self.output_format(message)
            ls.insert(0, 'Error')
            self.write(ls)
            return

        self.write("ERROR: " + self.output_format(message))

    def critical(self, message):
        if self.output_is_database:
            self.write(self.output_format(message).insert(0, 'Critical'))
            return

        self.write("CRITICAL: " + self.output_format(message))

    def output_format(self, message):
        current_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        msg = current_time + ' | ' + self.user + ' | '

        if self.filename != "":
            msg += self.filename + ' | '

        msg += message + '\n'

        if not self.output_is_database:
            return msg

        return [current_time, self.user, self.filename, message]

    # 输出函数
    def write(self, content):
        if not self.output_is_database:
            Logger.file_write(content)
        else:
            self.database_write(content)

    # 输出到文本文档
    @staticmethod
    def file_write(content):
        filename = time.strftime('%Y-%m-%d', time.localtime(time.time()))
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

    # 删除数据库表格
    @staticmethod
    def database_reset(config_filename):
        conn = Logger.setup_connection(config_filename)
        cursor = conn.cursor()
        drop_table = """DROP TABLE IF EXISTS LOGGING"""
        cursor.execute(drop_table)

    # 建立数据库表格
    @staticmethod
    def database_setup(config_filename):
        conn = Logger.setup_connection(config_filename)
        cursor = conn.cursor()

        create_table = """CREATE TABLE IF NOT EXISTS LOGGING(
                            LEVEL  CHAR(8),
                            TIME  CHAR(8),
                            USER  CHAR(16),
                            FILENAME  CHAR(32),
                            MESSAGE  CHAR(80))"""

        cursor.execute(create_table)
        conn.commit()

    # 输出到数据库
    def database_write(self, content):
        conn = Logger.setup_connection(self.config_filename)
        cursor = conn.cursor()

        insert_values = """INSERT INTO LOGGING(LEVEL, TIME, USER, FILENAME, MESSAGE)
                        VALUES(%s, %s, %s, %s, %s)"""

        cursor.execute(insert_values, (content[0], content[1], content[2], content[3], content[4]))

        conn.commit()

    # 建立连接
    @staticmethod
    def setup_connection(config_filename):
        config = BOF_ConfigReader.ConfigReader(config_filename)
        host = config.get_section("database").get_value('host')
        port = config.get_section("database").get_value('port')
        user = config.get_section("database").get_value('user')
        password = config.get_section("database").get_value('password')
        db = config.get_section("database").get_value('db')
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
        return conn

    # 在程序中直接输出数据库的内容
    def database_output(self):
        conn = Logger.setup_connection(self.config_filename)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM LOGGING""")
        rows = cursor.fetchall()

        for row in rows:
            print(row)
