from log4py import create_logger, SMTPHandler
import logging
stream = logging.StreamHandler()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(stream)
logger.info("root log")


params = {
    "mailhost": ("smtp.163.com", 25), "fromaddr": '***********@163.com',
    "toaddrs": ['****@outlook.com'], "subject": "服务器异常告警",
    "credentials": ('***********', '********')
}
# log = create_logger(__name__, handler=SMTPHandler(**params), level="error")
from log4py import FileHandler
log = create_logger(__name__, handler=FileHandler("1.log"))

log.info("hello world")

def func():
    log.error("hello function")

@create_logger()
# @create_logger(attr="log", logger_name="{name} hello")
@create_logger(attr="log")
class A:
    def __init__(self):
        self.log.info("hello class")
        self.logger.info("hello class")

func()
A()
