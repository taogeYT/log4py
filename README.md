## Log For Python

### Installation:
    pip install log4py

### Usage:
```python
from log4py import Logger
Logger.set_level("INFO")
log = Logger.get_logger(__name__)
log.info("hello logger")

@Logger.class_logger()
class LogTest:
    def __init__(self):
        self.logger.info("hello class logger")
LogTest()
```

output:     

    2020-03-28 23:39:07 __main__.<module>(demo.py:28) WARNING: hello logger    
    2020-03-28 23:39:07 __main__.LogTest.__init__(demo.py:34) WARNING: hello class logger


logger config

```python
from log4py import Logger
config = {
    "handlers": {"file_handler": {"class": "logging.FileHandler", 'filename': 'demo.log'}},
    "loggers": {'__main__': {"level": "INFO", "handlers": ["file_handler"], 'propagate': False}}
}
Logger.configure(**config)
log = Logger.get_logger(__name__)
log.info("hello logger")
```

overlay default config

    Logger.dict_config(dict_config)
OR

    Logger.file_config("logger.conf")


