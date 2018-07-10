# -*- coding: utf-8 -*-
"""
mylog module
1. 日志重复打印问题，是因为对同一个log实例，多次添加handler造成的。
2. 并且日志存在继承关系，会对子log产生影响，子log不仅执行自身的handler，
也会执行上层的handler一直到找到root的handler。
本模块默认自动继承开关默认关闭，不会存在冲突问题
"""
__author__ = "liyatao"
__version__ = "1.0.6"
__all__ = ["create_logger", "FileHandler", "SMTPHandler"]

import logging
import os
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler
from logging import StreamHandler

_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "error": logging.ERROR
}

_format = {
    "module": ('%(asctime)s %(levelname)s %(name)s(%(funcName)s): %(message)s', '%Y-%m-%d %H:%M:%S'),
    "class": ('%(asctime)s %(levelname)s %(name)s: %(message)s', '%Y-%m-%d %H:%M:%S')
}


class FileHandler(RotatingFileHandler):
    _handlers = {}

    def __new__(cls, filename="main.log", *args, **kw):
        # print(filename)
        keyname = os.path.normpath(filename)
        cls._handlers[keyname] = cls._handlers.get(keyname, object.__new__(cls))
        return cls._handlers[keyname]

    def __init__(self, filename="main.log", maxBytes=20*1024*1024, backupCount=5):
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


def _gen_logger(name, level, ltype, fmt, handler):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(_add_handler(ltype, fmt, handler))
        logger.setLevel(_levels[level])
        logger.propagate = False
    return logger


def bind_logger_to_object(*, level="info", fmt=None, attr="logger", handler=None):
    """类装饰器，绑定logger"""
    def decorator(instance):
        if instance.__module__ == "__main__":
            name = "%s(%s)" % ("main", instance.__name__)
        else:
            name = "%s(%s)" % (instance.__module__, instance.__name__)
        logger = _gen_logger(name, level, "class", fmt, handler)
        setattr(instance, attr, logger)
        return instance
    return decorator


def create_logger_by_name(name, *, level="info", fmt=None, handler=None):
    """创建logger对象"""
    if name == "__main__":
        name = "main"
    return _gen_logger(name, level, "module", fmt, handler)


def create_logger(*args, **kw):
    """
    create_logger(attr="logger", level="info", fmt=None, handler=None, config=None) -> decorator to bind logger
    create_logger(name, level="info", fmt=None, handler=None, config=None) -> a logger instance
    filehandler = FileHandler()
    filelog = create_logger(__name__, handler=filehandler, level="warn")

    @create_logger(attr="log")
    class A:
        pass

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
