import os
import sys
import pandas as pd
import  numpy as np

'''Defining the name of common constant variable for trainging pipeline'''

TARGET_COLUMN='Result'
PIPELINE_NAME: str='NetworkSecurity'
ARTIFACTS_DIR:str='Artifacts'
FILE_NAME: str='phisingData.csv'

TRAIN_FILE_NAME: str='train.csv'
TEST_FILE_NAME: str='test.csv'

SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yml")

'''Dtaa Ingestion related constants starts with Data_Ingestion Variable names.
This variables are constants throughout the enitre project'''

## Data Ingestion Constants
DATA_INGESTION_COLLECTION_NAME: str = 'NetworkData'
DATA_INGESTION_DATABASE_NAME: str="SAROJ"
DATA_INSGESTION_DIR_NAME: str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str ="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float =0.2

"""Name of Constant Validation Variable"""
DATA_VALIDATION_DIR_NAME: str="data_validation"
DATA_VALIDATION_VALID_DIR: str="Valid"
DATA_VALIDATION_INVALID_DIR: str="Invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str="report.yaml"

