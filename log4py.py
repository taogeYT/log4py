# -*- coding: utf-8 -*-
"""
mylog module
1. 日志重复打印问题，是因为对同一个log实例，多次添加handler造成的。
2. 并且日志存在继承关系，会对子log产生影响，子log不仅执行自身的handler，
也会执行上层的handler一直到找到root的handler。
本模块默认自动继承开关默认关闭，不会存在冲突问题
"""
from enum import Enum

__author__ = "liyatao"
__version__ = "1.1.2"
__all__ = ["create_logger", "FileHandler", "SMTPHandler"]

import logging
import os
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler
from logging import StreamHandler
LOG_ENV_VALUE = os.getenv("PY_LOG_LEVEL", "info")
# print(LOG_ENV_VALUE, os.getenv("PY_LOG_LEVEL"))
# _levels = {
#     "debug": logging.DEBUG,
#     "info": logging.INFO,
#     "warn": logging.WARN,
#     "error": logging.ERROR
# }
# _levels.update({None: _levels.get(LOG_ENV_VALUE, logging.INFO)})
_format = {
    "module": ('%(asctime)s %(levelname)s %(name)s.%(funcName)s: %(message)s', '%Y-%m-%d %H:%M:%S'),
    "class": ('%(asctime)s %(levelname)s %(name)s.%(funcName)s: %(message)s', '%Y-%m-%d %H:%M:%S')
}


class LogLevel(Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warn = logging.WARN
    error = logging.ERROR


class FileHandler(RotatingFileHandler):
    _handlers = {}

    def __new__(cls, filename="main.log", *args, **kw):
        # print(filename)
        keyname = os.path.normpath(filename)
        cls._handlers[keyname] = cls._handlers.get(keyname, object.__new__(cls))
        return cls._handlers[keyname]

    def __init__(self, filename="main.log", maxBytes=20*1024*1024, backupCount=5):
        """
        from log4py import FileHandler
        filehandler = FileHandler("1.log")
        log = create_logger(__name__, handler=filehandler)
        """
        super().__init__(filename, maxBytes, backupCount)


def _add_handler(ltype, fmt, handler):
    # handler = logging.StreamHandler() if filename is None else MyFileHandler(filename, maxBytes=maxBytes*1024*1024, backupCount=backupCount)
    if handler is None:
        handler = StreamHandler()
    if fmt is None:
        formatter = logging.Formatter(*_format[ltype])
    else:
        formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    return handler


def _gen_logger(name, level, ltype, fmt, handler, single):
    logger = logging.getLogger(name)
    if not logger.handlers or not single:
        logger.addHandler(_add_handler(ltype, fmt, handler))
        # logger.setLevel(_levels[level])
        logger.setLevel(LogLevel[level].value)
        logger.propagate = False
    return logger


def bind_logger_to_object(*, level=LOG_ENV_VALUE, fmt=None, handler=None, single=True, attr="logger", logger_name=None):
    """类装饰器，绑定logger"""
    def decorator(instance):
        # if instance.__module__ == "__main__":
        #     name = "%s(%s.%s)" % ("main", instance.__name__, attr)
        # else:
        #     name = "%s(%s.%s)" % (instance.__module__, instance.__name__, attr)

        module_name = "main" if instance.__module__ == "__main__" else instance.__module__
        fstring = "{module_name}.{instance_name}" if attr == "logger" else "{module_name}.{instance_name}<{attr_name}>"
        name = fstring.format(module_name=module_name, instance_name=instance.__name__, attr_name=attr)

        # if logger_name is None:
        #     _name = "{}[{}]".format(name, attr) if attr != "logger" else name
        # else:
        #     _name = logger_name.format(name=name)
        _name = name
        logger = _gen_logger(_name, level, "class", fmt, handler, single)
        setattr(instance, attr, logger)
        return instance
    return decorator


def create_logger_by_name(name, *, level=LOG_ENV_VALUE, fmt=None, handler=None, single=True):
    """创建logger对象"""
    if name == "__main__":
        name = "main"
    return _gen_logger(name, level, "module", fmt, handler, single)


def create_logger(*args, **kw):
    """
    create_logger(attr="logger", level="info", fmt=None, handler=None, config=None) -> decorator to bind logger
    create_logger(name, level="info", fmt=None, handler=None, config=None) -> a logger instance

    from log4py import FileHandler
    filehandler = FileHandler() # filename='main.log'
    filelog = create_logger(__name__, handler=filehandler, level="warn")

    @create_logger()
    @create_logger(attr="log", logger_name="{name} user define logger name")
    class A:
        pass

    # 阿里云邮箱服务器，阿里云服务器限制25端口，smtp服务器可以使用("smtp.mxhichina.com", 80)
    from log4py import SMTPHandler
    mailhandler = SMTPHandler(("smtp.163.com", 25), '180********@163.com', ['****@outlook.com'], "服务器异常告警", credentials=('180********', '*******'))
    maillog = create_logger(__name__, handler=mailhandler)
    maillog.info("hi,", exc_info=True)
    """
    if args:
        if isinstance(args[0], str):
            return create_logger_by_name(*args, **kw)
        else:
            raise TypeError("positional argument 'name' must be 'str' object")
    else:
        return bind_logger_to_object(**kw)
