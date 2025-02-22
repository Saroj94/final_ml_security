import sys
import logging
import traceback
from ..logging import logger  # Use relative import

# Create own exception class to handle the exception
class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail, error):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_detail = error_detail
        self.error = error

        _, _, self.exc_tb = sys.exc_info()
        self.traceback_str = ''.join(traceback.format_tb(self.exc_tb))

    def __str__(self):
        return f"{self.error_message}: {self.error_detail}\nTraceback: {self.traceback_str}"