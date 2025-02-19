import sys
import logging
import os
from networksecurity.logging import logger

##create own exception class to handle the exception
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info() ##exc_info(): this has three values and we only require the exc_tb

        self.lineno=exc_tb.tb_lineno ##get the line number where the exception occured
        self.file_name=exc_tb.tb_frame.f_code.co_filename ##get the file name where the exception occured

    ##string representation of the exception: this str error message will be called when we get sys error
    def __str__(self):
        return f'Error occured in python script name {self.file_name} at line number {self.lineno} and error message is {self.error_message}'
    

if __name__ == '__main__':
    try:
        logger.logging.info('This is the first log')    
        a=1/0
        print('This will not be printed',a)
    except Exception as e:
        raise NetworkSecurityException('Division by zero',e) 