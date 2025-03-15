import os
import sys
import certifi
ca=certifi.where()
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi import FastAPI,File,UploadFile,Request
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline=train_pipeline.run_pipeline()
        return Response("Training Pipeline Completed Successfully")
    except Exception as e:
        raise NetworkSecurityException("Error in training pipeline", e)

##batch prediction
@app.post('/predict')
async def predict_route(request:Request, file:UploadFile=File(...)):
    try:
        ##load file
        df=pd.read_csv(file.file)
        ##load the preprocessor
        preprocessor = load_object("final_model/preprocessor.pkl")
        ##load the model
        final_model = load_object("final_model/model.pkl")

        ##object of the NetworkModel which will be used to predict
        network_model = NetworkModel(preprocessor=preprocessor,model=final_model)
        ##print 
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        ##predicted column
        df['predicted_column']=y_pred


        ##create directory name to save the output file
        output_dir="prediction_output"
        ##create outputfile name
        output_file=os.path.join(output_dir,"output_file.csv")
        ##create directory if not exists
        os.makedirs(output_dir,exist_ok=True)
        ##save the file as csv
        df.to_csv(output_file,index=False)

        ##display the table
        table_html=df.to_html(classes="table table-striped")
        ##print the table
        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
      
    except Exception as e:
        raise NetworkSecurityException(e,sys)

if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)

