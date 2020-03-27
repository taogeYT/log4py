## Log For Python

### Installation:
    pip install log4py

### Usage:
    from log4py import Logger
    log = Logger.get_logger(__name__)
    log.warning("hello logger")
    
    @Logger.class_logger()
    class LogTest:
        def __init__(self):
            self.logger.warning("hello class logger")
    LogTest()

OUTPUT:     

    2020-03-28 23:39:07 __main__.<module>(demo.py:28) WARNING: hello logger    
    2020-03-28 23:39:07 __main__.LogTest.__init__(demo.py:34) WARNING: hello class logger


logger config

    Logger.dict_config("logger.conf")
OR

    Logger.file_config("logger.conf")
