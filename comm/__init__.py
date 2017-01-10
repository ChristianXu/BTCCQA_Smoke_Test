__author__ = 'sara'

import logging
import os
import time

prjDir = os.path.dirname(os.path.dirname(__file__))
__result_path = os.path.join(prjDir, "result")
log_path = os.path.join(__result_path, (time.strftime('%Y%m%d%H%M%S', time.localtime())))


def __set_log():
    # result_path = os.path.join(prjDir, "result")
    if os.path.exists(log_path) is False:
        os.makedirs(log_path)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create handler,write log
    fh = logging.FileHandler(os.path.join(log_path, "outPut.log"))
    out = logging.StreamHandler()
    # Define the output format of formatter handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - line%(lineno)d: %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    out.setFormatter(formatter)
    out.setLevel(logging.INFO)

    logger.addHandler(fh)
    logger.addHandler(out)

    return logger

__set_log()

__all__ = ['EXCELTestRunner', 'Info', 'Init', 'get_driver', 'open_url', 'get_element', 'get_elements', 'get_url',
           'is_page_loaded', 'my_assert', 'Template', 'SendEmail', ]

from .common import Info, get_driver, open_url, get_element, get_elements, get_url, is_page_loaded, my_assert
from .EXCELTestRunner import EXCELTestRunner
from .BaseTest import BaseTest
from .DRIVER import Init
from .Send import Template, SendEmail
