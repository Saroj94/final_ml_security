import logging
import os
from datetime import datetime


##Logging file name that i want to create with the below format
LOG_FILE=f'{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log'

##create path for the log file
LOG_PATH=os.path.join(os.getcwd(),'logs',LOG_FILE)

##create folder to sepecifically save the logs
os.makedirs(LOG_PATH,exist_ok=True)

##create the log file path
LOG_FILE_PATH=os.path.join(LOG_PATH,LOG_FILE)

##set the basic configuration for the logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s'
)