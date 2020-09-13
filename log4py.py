# encoding: utf-8
"""
@time: 2020/3/10 10:43 下午
@desc:
"""
__author__ = "liyatao"
__version__ = "2.2"
__all__ = ["Logger", "Level", "DefaultConfig"]

import logging.config
import logging
import os


class Level:
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class DefaultConfig(object):
    version = 1
    disable_existing_loggers = False
    incremental = False

    class Formatter:
        name = "default"
        format = "%(asctime)s %(levelname)s %(name)s.%(funcName)s(%(filename)s:%(lineno)d): %(message)s"
        datefmt = '%Y-%m-%d %H:%M:%S'
        class_name = "logging.Formatter"

    class Handler:
        name = "stdout"
        formatter = "default"
        class_name = 'logging.StreamHandler'

    class Root:
        handlers = ["stdout"]
        level = os.getenv("PY_LOG_LEVEL", "WARNING")

    @staticmethod
    def get_config():
        default_config = {
            'version': DefaultConfig.version,
            'disable_existing_loggers': DefaultConfig.disable_existing_loggers,
            'incremental': DefaultConfig.incremental,
            'formatters': {DefaultConfig.Formatter.name: {
                'class': DefaultConfig.Formatter.class_name,
                'format': DefaultConfig.Formatter.format,
                'datefmt': DefaultConfig.Formatter.datefmt}},
            'handlers': {DefaultConfig.Handler.name: {
                'class': DefaultConfig.Handler.class_name,
                'formatter': DefaultConfig.Handler.formatter}},
            'root': {'handlers': DefaultConfig.Root.handlers,
                     "level": DefaultConfig.Root.level},
            'loggers': {
                # '__main__': {"level": "DEBUG", "handlers": ['stdout']},
            }
        }
        return default_config


def make_formatters(config):
    """
    {'class': 'logging.Formatter', 'format': Default.format, 'datefmt': '%Y-%m-%d %H:%M:%S'}
    """
    for key in config:
        config[key] = {'class': 'logging.Formatter', 'datefmt': '%Y-%m-%d %H:%M:%S', **config[key]}
    return config


def make_handlers(config):
    """
    {'class': 'logging.StreamHandler', 'formatter': 'default'}
    """
    for key in config:
        config[key] = {'class': 'logging.StreamHandler', 'formatter': 'default', **config[key]}
    return config


class Logger(object):
    logging.config.dictConfig(DefaultConfig.get_config())
    root = logging.root

    @classmethod
    def configure(cls, root=None, handlers=None, formatters=None, loggers=None):
        """
        配置日志，更新形式写入log4py模块的默认配置
        :param root: dict, root logger 配置
        :param handlers: dict, handler 配置
        :param formatters: dict, formatter 配置
        :param loggers: dict, 定制 logger 单独配置

        加载配置示例
        from log4py import Logger
        config = {
            "handlers": {"file": {"class": "logging.FileHandler", 'filename': 'run.log'}},
            "root": {"handlers": ["default", "file"], "level": "INFO"}
        }
        Logger.configure(**config)

        常用handler配置示例
        1. file handler
        handlers = {"file": {'class': 'logging.FileHandler', 'filename': "run.log"}}
        2. rotating file handler
        handlers = {
            "rotating_file": {
                'class': 'logging.handlers.RotatingFileHandler',
                "filename": "run.log", "maxBytes": "20*1024*1024", "backupCount": 5}
        }
        3. email handler, 注意：阿里云邮箱服务器限制25端口，smtp服务器使用("smtp.mxhichina.com", 80)
        handlers = {
            "email": {
                "class": "logging.handlers.SMTPHandler", "mailhost": ("smtp.163.com", 25),
                "fromaddr": '****@163.com', "toaddrs": ['****@outlook.com'],
                "subject": "应用告警", "credentials": ('****', '****')
            }
        }
        """
        root = {} if root is None else root
        handlers = {} if handlers is None else handlers
        formatters = {} if formatters is None else formatters
        loggers = {} if loggers is None else loggers
        default_config = DefaultConfig.get_config()
        default_config["formatters"].update(make_handlers(formatters))
        default_config["handlers"].update(make_handlers(handlers))
        default_config["root"].update(root)
        default_config["loggers"].update(make_handlers(loggers))
        cls.dict_config(default_config)
        return default_config

    @classmethod
    def dict_config(cls, config):
        logging.config.dictConfig(config)
        cls.not_config = False

    @classmethod
    def file_config(cls, file):
        logging.config.fileConfig(file)
        cls.not_config = False

    @classmethod
    def set_level(cls, level):
        """设置全局日志级别"""
        logging.root.setLevel(level)

    @classmethod
    def get_logger(cls, name=None):
        """
        log = Logger.get_logger(__name__)
        log.warning("hello logger")
        """
        return logging.getLogger(name)

    @classmethod
    def class_logger(cls, attr="logger"):
        """
        @Logger.class_logger()
        class A:
            def run(self):
                self.logger.warning("hello class logger")
        """
        def decorator(class_obj):
            name = f"{class_obj.__module__}.{class_obj.__name__}"
            setattr(class_obj, attr, logging.getLogger(name))
            return class_obj
        return decorator


if __name__ == '__main__':
    @Logger.class_logger()
    class A:
        def __init__(self):
            self.logger.info("hello class logger")
    log = Logger.get_logger(__name__)
    log.setLevel(Level.INFO)
    log.info("hello logger")
    A()
