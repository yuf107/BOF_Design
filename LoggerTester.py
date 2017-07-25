import unittest
import BOF_Logger


class TestLogger(unittest.TestCase):
    # 测试输出到数据库的默认表格"logging"
    def test_database_logging(self):
        logger = BOF_Logger.Logger('LoggerConfig')
        logger.error("This is a test for database logging.")
        logger.critical('Logging into default table: logging. ')

    # 测试输出到用户自定义的表格
    def test_database_given_table(self):
        logger = BOF_Logger.Logger('ConfigWithTable')
        logger.debug("A test for database given table.")
        logger.info("Another test for database given table.")
        logger.warning('Logging into the table given by user.')

    # 测试默认输出：输出到文本文档，无配置文件
    def test_default_logging(self):
        logger = BOF_Logger.Logger()
        logger.debug("This is a test for default logging.")
        logger.info('Without config file, the logger is set to all default values.')
        logger.warning('Output is sent to text files. The column "filename" is empty.')

    # 测试输出到文本文档，有配置文件
    def test_file_logging(self):
        logger = BOF_Logger.Logger('FileConfig')
        logger.error('This is a test for file logging with config.')
        logger.critical('Output is sent to text files.')


if __name__ == '__main__':
    unittest.main()
