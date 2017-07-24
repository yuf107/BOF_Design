import unittest
import BOF_Logger
import BOF_ConfigReader
import time
import os


class TestLogger(unittest.TestCase):
    def test_file_write(self):
        time_list = []
        for i in range(5):
            time_list.append(time.strftime("%H-%M-%S", time.localtime(time.time())))
            BOF_Logger.Logger.file_write_test(time_list[i])
            time.sleep(1)

        for i in range(5):
            file = open(time_list[i])
            self.assertEqual(file.readlines()[0], time_list[i])
            file.close()

    @staticmethod
    def test_output_format():
        logger1 = BOF_Logger.Logger(None, "Some user", os.path.basename(__file__))
        print(logger1.output_format("This is a test of output_format function."))
        logger2 = BOF_Logger.Logger()
        print(logger2.output_format("This is a test of output_format function."))

    def test_file_logging(self):
        logger = BOF_Logger.Logger()
        logger.critical("This is a test of critical function.")
        expected = "CRITICAL: " + logger.output_format("This is a test of critical function.")

        current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        file = open(current_date)
        lines = file.readlines()
        self.assertEqual(lines[len(lines) - 1], expected)
        file.close()

    def test_config(self):
        config = BOF_ConfigReader.ConfigReader("LoggerConfig")
        message = config.get_section("init").get_value("Message")
        logger = BOF_Logger.Logger()
        logger.warning(message)
        expected = "WARNING: " + logger.output_format(message)

        current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        file = open(current_date)
        lines = file.readlines()
        self.assertEqual(lines[len(lines) - 1], expected)
        file.close()

    def test_database_setup(self):
        BOF_Logger.Logger.database_setup('LoggerConfig')

    def test_database_write(self):
        logger = BOF_Logger.Logger(database_config="LoggerConfig")
        logger.database_write(['Warning', '11:00:00',
                               'user name', 'LoggerTester.py',
                               'This is a test for database write.'])

    def test_database_logging(self):
        logger = BOF_Logger.Logger(database_config='LoggerConfig')
        logger.error("This is a test for database logging.")

        logger.database_output()


if __name__ == '__main__':
    unittest.main()
