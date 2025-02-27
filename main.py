"""Data Ingestion checker"""
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataValidationConfig
from networksecurity.component.data_ingestion import DataIngestion
from networksecurity.component.data_validation import DataValidation

import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info('Initiate the data ingestion')
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)

        logging.info("Data Inititation completed")
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Data validation is initiated")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data validation is completed")
        print(data_validation_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)