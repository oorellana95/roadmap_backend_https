"""Logger Class"""
import logging

_logger = logging.getLogger(__name__)


class Logger:
    def __init__(self):
        self.project = "rule-of-thumb"
        self.sector = "backend"

    def error(self, message: str, code: str = None):
        """Log an error message with the standard output format."""
        _logger.setLevel(logging.ERROR)
        output = self.output(logger_type="Error", message=message, code=code)
        _logger.error(output)

    def warning(self, message: str, code: str = None):
        """Log a warning message with the standard output format."""
        _logger.setLevel(logging.WARNING)
        output = self.output(logger_type="Warning", message=message, code=code)
        _logger.warning(output)

    def debug(self, message: str, code: str = None):
        """Log a debug message with the standard output format."""
        _logger.setLevel(logging.DEBUG)
        output = self.output(logger_type="Debug", message=message, code=code)
        _logger.debug(output)

    def info(self, message: str, code: str = None):
        """Log an information message with the standard output format."""
        _logger.setLevel(logging.INFO)
        output = self.output(logger_type="Info", message=message, code=code)
        _logger.info(output)

    def output(self, logger_type: str, message: str, code: str):
        """Output message with code and value."""
        output = f"{logger_type} in {self.project}:{self.sector};"
        if code:
            output = output + f"\n{logger_type} code: {code};"
        return output + f"\nMessage: {message}"


logger = Logger()
