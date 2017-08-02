import BOF_Logger
import traceback
import os


class ExceptionHandler:
    def __init__(self, logger_config=None):
        self.logger = BOF_Logger.Logger(logger_config)

    # 整理异常信息
    @staticmethod
    def exc_format(err):
        exc_info = traceback.format_exc()
        exc_name = repr(err).split('(')[0]
        line_number = int(exc_info.split('line ')[1].split(',')[0])
        exc_description = repr(err).split('(')[1].strip(')').strip(',').strip("'").strip('"')

        msg = exc_name + ' at line ' + str(line_number) + ': ' + exc_description

        return msg

    # 把异常信息输入到程序运行记录中
    def log_exc(self, err):
        msg = ExceptionHandler.exc_format(err)
        self.logger.error(msg)

    # 检查文件是否存在 返回True or False 同时输出到Logger
    def check_file(self, filename):
        file_exists = os.path.exists(filename)

        if file_exists:
            msg = 'File %s exists.' % filename
        else:
            msg = 'File %s does not exist.' % filename

        self.logger.info(msg)

        return file_exists
