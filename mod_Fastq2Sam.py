#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2017/8/10 0010'
__author__ = 'kui.wu'

import datetime
import logging
import os
import time
from BOF_Logger import Logger
import subprocess

from BOF_ConfigReader import ConfigReader
from BOF_Timer import Timer
from BOF_ExceptionHandler import ExceptionHandler
def bio_main(sample_id, workflow_class, fastq1, fastq2, out_put, *args, **kwargs):
    """
    convert fastq file to sam file
    :param sample_id: 样本ID
    :param workflow_class: 流程级
    :param fastq1: fastq R1 file
    :param fastq2: fastq R2 file
                "message": "ok",
    common_cnf = ConfigReader("../conf/common.conf")
    bwa = common_cnf.get_value("APPLICATITON", "bwa")
    ## init mode configure
    mod_conf = ConfigReader("../conf/mod_Fastq2Sam.conf")
    bwa_thread = mod_conf.get_value(workflow_class, "bwa_t")

    # set up bof_logger object 
    id_dict = kwargs
    conf_name = '../conf/mod_Fastq2Sam.conf'
    mode_id = mod_conf.get_value('all', 'mode_id')
    id_dict['module_id'] = mode_id
    bof_logger = Logger(conf_name, level='info', other=id_dict)
    bof_logger.info('test')

    # set up timer object
    timer = Timer(conf_name, id_dict)
    timer.start_timing()

    exc_handler = ExceptionHandler(conf_name, other=id_dict)

    os.makedirs(os.path.abspath(os.path.dirname(out_put)),exist_ok=True)

    try:
        """run bwa"""
        sample_sam = os.path.abspath(out_put + f"/{sample_id}.sam")
        ## check the fastq files
        if not (os.path.exists(fastq1) and os.path.exists(fastq2)):
            logger.error(f"{fastq1} and {fastq2} not all exist!")
            bof_logger.error(f"{fastq1} and {fastq2} not all exist!")
            return {"code": 1, "message": "fastq file not exist!"}
        ## mv old sam file

        logger.info(shell_cmd)
        bof_logger.info(shell_cmd)
        p = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        logger.info(out)
        logger.warning(err)
        bof_logger.info(out)
        bof_logger.warning(str(err))
        ## process not terminated normally

        timer.end_timing()  # end the timing process and write result into database

        if not p.returncode == 0:
            logger.error(f"{shell_cmd} crashed")
            bof_logger.error(f"{shell_cmd} crashed")
            return {"code":1, "message": "run bwa app failed!"}

        logger.info(f"{shell_cmd} finished!")
        bof_logger.info(f"{shell_cmd} finished!")

        return  {"code":0,
                 "message": "ok",
                 "sam": sample_sam}
    except Exception as e:
        logger.exception(f"{sample_id} run mod_fastq2sam failed!")
        bof_logger.error(f"{sample_id} run mod_fastq2sam failed!")
        exc_handler.handle(e)
        return {"code":1, "message": "run mod_fastq2sam failed!"}

    finally:
        pass

    # timer.end_timing()  
    # 在这里执行结束计时会出现未知原因的错误，因此放在上面try block中


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - File: %(filename)s - %(funcName)s() - Line: %(lineno)d -  %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    print(bio_main("ConTanSimu_9_0.50", "IC", "/gendata/wukui/FASTQ/ConTanSimu_9_0.50_R1.fastq.gz",
                   "/gendata/wukui/FASTQ/ConTanSimu_9_0.50_R2.fastq.gz", "/gendata/wukui",
                   bia_id=0, flowset_id=0, flow_id=0, node_id=0))
