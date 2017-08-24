import traceback
import time
import getpass
import BOF_Logger


class ExceptionHandler:
    # 构造函数
    def __init__(self, config, other=None):
        self.logger = BOF_Logger.Logger(config, other=other)

    # 整理异常信息
    @staticmethod
    def exc_format(err):
        exc_info = traceback.format_exc()
        exc_name = repr(err).split('(')[0]
        line_number = int(exc_info.split('line ')[1].split(',')[0])
        exc_description = repr(err).split('(')[1].strip(')').strip(',').strip("'").strip('"')
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        user = getpass.getuser()

        result = exc_name + ' at line ' + str(line_number) + ': ' + exc_description
        return result

    # 把异常信息输入到用户提供的数据库中
    def handle(self, err):
        self.logger.critical(ExceptionHandler.exc_format(err))
