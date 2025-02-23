"This file has different functions that fetch data and split data."
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

##mongo db url
MONGO_DB_URL=os.getenv('MONGODB_URL')

class DataIngestion:
    ## initialize data ingestion config setting
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    ## Function reads the data from mongodb database and export it as dataframe
    def export_collection_as_dataframe(self):
        """
        This function reads the data from Mongodb Database and export it into dataframe
        """
        try:
            ##initialize the object of database, ccollection and mongo client
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            ##get collection name
            collection=self.mongo_client[database_name][collection_name]
            ##exporting into dataframe
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_data_to_feature_store(self,dataframe: pd.DataFrame):
        try:
            ##object of file path name 
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            ##set folder name as
            #  feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            ##create folder
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_ratio
            )
            logging.info("Performed train test split on the dataframe")
            logging.info('Exited split_data_as_train_test method of Data Ingestion Class')

            ##setting up file directory path because to save/store the train_set file
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            ##creating folder
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting train and test file path.")

            ##exporting as train set and test set as csv file into the dirtory
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)

            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info("Train_set and Test_set successfully save in respective file path.")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            ##data into dataframe
            dataframe=self.export_collection_as_dataframe()
            ##dataframe
            df=self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(df)

            ##artifact
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path
                                                        )
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
