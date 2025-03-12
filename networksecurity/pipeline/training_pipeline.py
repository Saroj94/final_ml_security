import os 
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.component.data_ingestion import DataIngestion
from networksecurity.component.data_validation import DataValidation
from networksecurity.component.data_transformation import DataTransformation
from networksecurity.component.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)


class TrainingPipeline:
    def __init__(self):
        ## Initialize the configuration objects
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            ## initialize the data ingestion configuration
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            ## initialize the data ingestion object
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            ## start the data ingestion process
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException("Error in data ingestion", e)
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            ## initialize the data validation configuration
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            ## initialize the data validation object
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            ## start the data validation process
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException("Error in data validation", e)
        
    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        try:
            ## initialize the data transformation configuration
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            ## initialize the data transformation object
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                      data_transformation_config=data_transformation_config)
            ## start the data transformation process
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException("Error in data transformation", e)
        
    def start_model_training(self, data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config: ModelTrainerConfig=ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config)
            
            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                       model_trainer_config=self.model_trainer_config)
            
            model_trainer_artifact=model_trainer.initiate_model_training()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException("Error in model training", e)
        
    def run_pipeline(self):
        try:
            ## start the data ingestion process
            data_ingestion_artifact = self.start_data_ingestion()
            ## start the data validation process
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            ## start the data transformation process
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            ## start the model training process
            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException("Error in training pipeline", e)