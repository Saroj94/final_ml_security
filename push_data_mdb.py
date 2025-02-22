import os
import sys
import json
import pymongo
import certifi
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")  # ✅ Load from .env file
print(f"🔗 Connecting to MongoDB: {MONGODB_URL}")

## Object of certifi
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        """ Convert CSV file to JSON format """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} not found")
            
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except FileNotFoundError as fe:
            print(f"❌ CSV file not found: {fe}")
            raise
        except Exception as e:
            print(f"❌ Error processing CSV file: {e}")
            raise
        
    def insert_data_mongodb(self, records, database, collection):
        """ Insert JSON data into MongoDB """
        try:
            self.database = database
            self.collection = collection
            self.records = records

            # ✅ Secure MongoDB connection
            self.mongo_client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=certifi.where())

            # ✅ Check connection
            self.mongo_client.admin.command('ping')
            print("✅ MongoDB Connection Successful")

            # Get database and collection
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            
            # Insert data
            self.collection.insert_many(self.records)
            return '✅ Data inserted successfully'
        except pymongo.errors.OperationFailure as e:
            print(f"❌ MongoDB Authentication Failed: {e}")
            raise
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            raise
        
if __name__ == '__main__':
    FILE_PATH = 'Network_data/phisingData.csv'
    DATABASE = 'SAROJ'
    Collection = 'NetworkData'

    networkobj = NetworkDataExtract()
    
    try:
        # Convert CSV to JSON
        records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
        print(f"📄 Converted {len(records)} records from CSV")

        # Insert into MongoDB
        no_of_records = networkobj.insert_data_mongodb(records=records, database=DATABASE, collection=Collection)
        print(no_of_records)

    except Exception as e:
        print(f"❌ Script Failed: {e}")