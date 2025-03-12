from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object,load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.clasification_metric import get_classification_score
import os
import sys
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (AdaBoostClassifier,RandomForestClassifier,GradientBoostingClassifier)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import r2_score
import mlflow

import dagshub
##initializing the daghub objct
dagshub.init(repo_owner='Saroj94', repo_name='final_ml_security', mlflow=True)


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                  data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    ##tracking function with mlflow
    def track_mlflow(self,best_model,classificationmetric):
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score

            mlflow.log_metric("f1 score",f1_score)
            mlflow.log_metric("Precision score",precision_score)
            mlflow.log_metric("Recall score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")

    ##define train_model function
    def train_model(self,x_train,y_train,x_test,y_test):
        ##Models to be used in our traing the model
        models={
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest":RandomForestClassifier(verbose=1),
            "Gradient Boosting":GradientBoostingClassifier(verbose=1),
            "Adaboost":AdaBoostClassifier(),
            "KNN":KNeighborsClassifier(),
            "SVM":SVC(),
            "Logistic Regression":LogisticRegression()
        }

        ##hyperparameter tunning
        params={
            "Decision Tree":{
                'criterion':['gini','entropy','log_loss'],
                #'splitter':['best', 'random'],
                #'max_features':['sqrt', 'log2']
            },
            "Random Forest":{
                #criterion:[“gini”, “entropy”, “log_loss”],
                #max_features{“sqrt”, “log2”, None},
                'n_estimators':[8,16,32,64,128,256]
            },
            "Gradient Boosting":{
                #loss:{‘log_loss’, ‘exponential’},
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                #criterion:[‘friedman_mse’, ‘squared_error’],
                #max_features:[‘sqrt’, ‘log2’]
                'n_estimators':[8,16,32,64,128,256]
            },
            "Adaboost":{
                'learning_rate':[.1,.01,.05,.001],
                'n_estimators':[8,16,32,64,128,256]
            },
            "SVM":{},
            "KNN":{},
            "Logistic Regression":{}
        }
        model_report: dict = evaluate_models(
            X_train=x_train,
            y_train=y_train,
            X_test=x_test,
            y_test=y_test,
            models=models,
            param=params)
        
        ##to get best model score from the dict
        best_model_score=max(sorted(model_report.values()))

        ##to get best model name from dict
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model=models[best_model_name]
        y_train_pred=best_model.predict(x_train)
        
        #clasification metric
        classification_train_metric=get_classification_score(y_actual=y_train,y_pred=y_train_pred)

        ##track the entire experiment with mlflow
        self.track_mlflow(best_model,classification_train_metric)


        y_test_pred=best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_actual=y_test,y_pred=y_test_pred)

        ##load preprocessor
        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)
        
        ##model pusher into a folder
        save_object("final_model/model.pkl",best_model)

        ##model trainer artifact
        Model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artiafct=classification_train_metric,
                             test_metric_artifact=classification_test_metric)
        logging.info(f"Model trainer artifact: {Model_trainer_artifact}")

        return Model_trainer_artifact
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            ##loading training array and testing array
            train_arr= load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            ##splitting x_train,x_test,y_train,y_test
            x_train,y_train,x_test,y_test=(
                train_arr[:, :-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            ##train model
            model=self.train_model(x_train,y_train,x_test,y_test)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
