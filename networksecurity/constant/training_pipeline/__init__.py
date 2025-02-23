import os
import sys
import pandas as pd
import  numpy as np

'''Defining the common constant variable for trainging pipeline'''

TARGET_COLUMN='Result'
PIPELINE_NAME: str='NetworkSecurity'
ARTIFACTS_DIR:str='Artifacts'
FILE_NAME: str='phisingData.csv'

TRAIN_FILE_NAME: str='train.csv'
TEST_FILE_NAME: str='test.csv'

'''Dtaa Ingestion related constants starts with Data_Ingestion Variable names.
This variables are constants throughout the enitre project'''

## Data Ingestion Constants
DATA_INGESTION_COLLECTION_NAME: str = 'NetworkData'
DATA_INGESTION_DATABASE_NAME: str="SAROJ"
DATA_INSGESTION_DIR_NAME: str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str ="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float =0.2

