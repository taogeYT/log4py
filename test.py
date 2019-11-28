from log4py import create_logger, SMTPHandler
import logging
stream = logging.StreamHandler()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(stream)

params = {
    "mailhost": ("smtp.163.com", 25), "fromaddr": '***********@163.com',
    "toaddrs": ['****@outlook.com'], "subject": "服务器异常告警",
    "credentials": ('***********', '********')
}
# log = create_logger(__name__, handler=SMTPHandler(**params), level="error")
# from log4py import FileHandler
# log = create_logger(__name__, handler=FileHandler("1.log"))
log = create_logger(__name__, level="error")

def func1():
    log.error("hello function")

@create_logger()
@create_logger(attr="log")
class A:
    def __init__(self):
        self.log.info("hello class")
        self.logger.info("hello class")
        self.elog()

    def elog(self):
        self.logger.info("hello")

logger.info("root log")
log.info("hello world")
logging.basicConfig(level=logging.WARNING)
logging.info("info")
func1()
A()
