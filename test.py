from log4py import create_logger


log = create_logger(__name__)

log.info("hello world")

def func():
    log.info("hello function")

@create_logger()
class A:
    def __init__(self):
        self.logger.info("hello class")


func()
A()
