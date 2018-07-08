from log4py import create_logger
import logging
ch = logging.StreamHandler()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(ch)
logger.info("root log")


log = create_logger(__name__)
log.info("hello world")

def func():
    log.info("hello function")

@create_logger(attr="log")
class A:
    def __init__(self):
        self.log.info("hello class")

func()
A()
