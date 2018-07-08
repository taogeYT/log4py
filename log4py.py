# -*- coding: utf-8 -*-
"""
mylog module
1. 日志重复打印问题，是因为对同一个log实例，多次添加handler造成的。
2. 并且日志存在继承关系，会对子log产生影响，子log不仅执行自身的handler，
也会执行上层的handler一直到找到root的handler。
本模块默认自动继承开关默认关闭，不会存在冲突问题
"""
__author__ = "liyatao"
__version__ = "1.0.4"
__all__ = ["create_logger"]

import logging
import os
# from logging import FileHandler
from logging.handlers import RotatingFileHandler

level = "info"
_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN
}
_format = {
    "module": ('%(asctime)s %(levelname)s %(name)s(%(funcName)s): %(message)s', '%Y-%m-%d %H:%M:%S'),
    "class": ('%(asctime)s %(levelname)s %(name)s: %(message)s', '%Y-%m-%d %H:%M:%S')
}

# class MyHandler(FileHandler):

#     @property
#     def baseFilename(self):
#         self._baseFilename = '{}-{}'.format(self._baseFilename, datetime.datetime.now().strftime("%Y%m%d%S"))
#         return self._baseFilename

#     @baseFilename.setter
#     def baseFilename(self, value):
#         self._baseFilename = value
#         return self._baseFilename


class MyHandler(RotatingFileHandler):
    _handlers = {}

    def __new__(cls, filename, *args, **kw):
        keyname = os.path.normpath(filename)
        cls._handlers[keyname] = cls._handlers.get(keyname, object.__new__(cls))
        return cls._handlers[keyname]


def _add_handler(ltype, filename, maxBytes, backupCount, fmt):
    handler = logging.StreamHandler() if filename is None else MyHandler(filename, maxBytes=maxBytes*1024*1024, backupCount=backupCount)
    if fmt is None:
        formatter = logging.Formatter(*_format[ltype])
    else:
        formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    return handler


def _gen_logger(name, level, ltype, filename, maxBytes, backupCount, fmt):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(_add_handler(ltype, filename, maxBytes, backupCount, fmt))
        logger.setLevel(_levels[level])
        logger.propagate = False
    return logger


def bind_logger_to_object(*, level=level, filename=None, maxMBytes=20, backupCount=5, fmt=None, attr="logger"):
    def decorator(instance):
        if instance.__module__ == "__main__":
            name = "%s(%s)" % ("main", instance.__name__)
        else:
            name = "%s(%s)" % (instance.__module__, instance.__name__)
        logger = _gen_logger(name, level, "class", filename, maxMBytes, backupCount, fmt)
        setattr(instance, attr, logger)
        return instance
    return decorator


def create_logger_by_name(name, *, level=level, filename=None, maxMBytes=20, backupCount=5, fmt=None):
    if name == "__main__":
        name = "main"
    return _gen_logger(name, level, "module", filename, maxMBytes, backupCount, fmt)


def create_logger(*args, **kw):
    """
    create_logger(attr="logger", level="info", fmt=None, filename=None, maxMBytes=20, backup=5) -> decorator to bind logger
    create_logger(name, level="info", fmt=None, filename=None, maxMBytes=20, backup=5) -> a logger instance
    """
    if args:
        if isinstance(args[0], str):
            return create_logger_by_name(*args, **kw)
        else:
            raise TypeError("positional argument 'name' must be 'str' object")
    else:
        return bind_logger_to_object(**kw)
