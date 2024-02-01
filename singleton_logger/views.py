import threading
import datetime

class LogLevel:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class LoggerImpl:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.log_file_path = None
        self.log_writer = None

    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    @classmethod
    def resetInstance(cls):
        with cls._lock:
            if cls._instance is not None:
                cls._instance.close()
                cls._instance = None

    def log(self, level, message):
        if self.log_writer is None:
            raise Exception("Log file not set. Call setLogFile() before logging.")
        timestamp = datetime.datetime.now()
        formatted_message = f"[{timestamp.strftime('%Y-%m-%dT%H:%M:%S')}] [{level}] {message}"
        self.log_writer.write(formatted_message + '\n')
        self.log_writer.flush()

    def getLogFile(self):
        return self.log_file_path

    def setLogFile(self, file_path):
        self.close()
        self.log_file_path = file_path
        self.log_writer = open(self.log_file_path, 'a')

    def flush(self):
        if self.log_writer is not None:
            self.log_writer.flush()

    def close(self):
        if self.log_writer is not None:
            self.log_writer.close()
            self.log_writer = None
