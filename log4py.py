# -*- coding: utf-8 -*-
"""
mylog module
1. 日志重复打印问题，是因为对同一个log实例，多次添加handler造成的。
2. 并且日志存在继承关系，会对子log产生影响，子log不仅执行自身的handler，
也会执行上层的handler一直到找到root的handler。
3. 基于上述原因，避免同一个模块中将"instance_log"或"class_log"和module_log同时使用。
"""
__author__ = "liyatao"
__version__ = "1.0.2"
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
    return logger


def class_log(level=level, filename=None, maxBytes=20, backupCount=5, fmt=None):
    def wrapper(instance):
        if instance.__module__ == "__main__":
            name = "%s(%s)" % ("main", instance.__name__)
        else:
            name = "%s(%s)" % (instance.__module__, instance.__name__)
        instance.logger = _gen_logger(name, level, "class", filename, maxBytes, backupCount, fmt)
        return instance
    return wrapper


def module_log(name, level=level, filename=None, maxBytes=20, backupCount=5, fmt=None):
    if name == "__main__":
        name = "main"
    return _gen_logger(name, level, "module", filename, maxBytes, backupCount, fmt)


def create_logger(*args, **kw):
    # print(args, kw)
    if args and isinstance(args[0], str):
        return module_log(*args, **kw)
    else:
        return class_log(**kw)
