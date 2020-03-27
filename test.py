import os
import unittest

from log4py import Logger, Level


class TestLogger(unittest.TestCase):
    log_file = "test.log"
    file = None

    @classmethod
    def setUpClass(cls):
        open(cls.log_file, mode="w", encoding="utf-8").close()
        cls.file = open(cls.log_file, mode="r", encoding="utf-8")
        file_handler = {'class': 'logging.FileHandler', 'filename': cls.log_file}
        Logger.configure(root={"handlers": ["file"]}, handlers={"file": file_handler})

    @classmethod
    def tearDownClass(cls):
        cls.file.close()
        os.remove(cls.log_file)

    def test_get_logger(self):
        log = Logger.get_logger(__name__)
        self.assertEqual(log.level, 0)
        message = "hello logger"
        log.warning(message)
        line = self.file.readline()
        self.assertTrue(message in line and "WARNING" in line)
        log.info(message)
        line = self.file.readline()
        self.assertEqual(line, "")
        log.setLevel(Level.INFO)
        log.info(message)
        line = self.file.readline()
        self.assertTrue(message in line and "INFO" in line)

    def test_class_logger(self):
        @Logger.class_logger()
        class A:
            @classmethod
            def warning_log(cls, msg):
                cls.logger.warning(msg)

            @classmethod
            def info_log(cls, msg):
                cls.logger.info(msg)
        a = A()
        self.assertEqual(a.logger.level, 0)
        message = "hello class logger"
        a.warning_log(message)
        line = self.file.readline()
        self.assertTrue(message in line and "WARNING" in line)
        a.info_log(message)
        line = self.file.readline()
        self.assertEqual(line, "")
        a.logger.setLevel(Level.INFO)
        a.info_log(message)
        line = self.file.readline()
        self.assertTrue(message in line and "INFO" in line)

