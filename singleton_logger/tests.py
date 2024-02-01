import unittest
from singleton_logger.views import LoggerImpl, LogLevel
import tempfile
import os

class TestLoggerImpl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.log_file_path = os.path.join(cls.temp_dir.name, "test.log")

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def setUp(self):
        LoggerImpl.resetInstance()
        LoggerImpl.getInstance().setLogFile(self.log_file_path)

    def tearDown(self):
        LoggerImpl.getInstance().close()
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_get_instance_method(self):
        instance = LoggerImpl.getInstance()
        self.assertIsNotNone(instance)

    def test_singleton_behavior(self):
        instance1 = LoggerImpl.getInstance()
        instance2 = LoggerImpl.getInstance()
        self.assertIs(instance1, instance2)

    def test_singleton_thread_safety(self):
        from concurrent.futures import ThreadPoolExecutor

        def get_instance(_):
            return LoggerImpl.getInstance()

        with ThreadPoolExecutor(max_workers=10) as executor:
            instances = list(executor.map(get_instance, range(10)))

        reference_instance = instances[0]
        for instance in instances[1:]:
            self.assertIs(reference_instance, instance)

    def test_reset_instance_method(self):
        instance1 = LoggerImpl.getInstance()
        LoggerImpl.resetInstance()
        instance2 = LoggerImpl.getInstance()
        self.assertIsNot(instance1, instance2)

    def test_log_method(self):
        logger = LoggerImpl.getInstance()
        logger.log(LogLevel.INFO, "Test log message")
        logger.flush()
        with open(self.log_file_path, 'r') as file:
            log_contents = file.read()
        self.assertIn("Test log message", log_contents)

    def test_set_log_file(self):
        logger = LoggerImpl.getInstance()
        logger.setLogFile(self.log_file_path)
        self.assertEqual(self.log_file_path, logger.getLogFile())

    def test_flush_method(self):
        logger = LoggerImpl.getInstance()
        logger.log(LogLevel.INFO, "Test log message")
        logger.flush()
        with open(self.log_file_path, 'r') as file:
            log_contents = file.read()
        self.assertIn("Test log message", log_contents)

    def test_close_method(self):
        logger = LoggerImpl.getInstance()
        logger.setLogFile(self.log_file_path)
        logger.close()
        with self.assertRaises(Exception):
            logger.log(LogLevel.INFO, "Test log message")

if __name__ == '__main__':
    unittest.main()
