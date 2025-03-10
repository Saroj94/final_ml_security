"""Data Ingestion checker"""
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.component.data_ingestion import DataIngestion
from networksecurity.component.data_validation import DataValidation
from networksecurity.component.data_transformation import DataTransformation
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.component.model_trainer import ModelTrainer
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

        logging.info("Data Transformation started")
        ##initializing the data transformation config
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        ##initializing data transformation
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        ##initiate data transformation method to get artifacts of data transformation
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data tarnsformation initiation completed")
        print(data_transformation_artifact)

        logging.info("Model training started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model training artifact created")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)