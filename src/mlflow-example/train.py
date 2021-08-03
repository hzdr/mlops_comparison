import os
import warnings
import sys

import numpy as np
import pandas as pd


from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet, LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import mlflow
import mlflow.sklearn 

from config import Config
import yaml
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

mlflow.set_tracking_uri("http://localhost:5000")

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    with open ("params.yaml", "r") as fd:
        params = yaml.safe_load(fd)

    np.random.seed(params['random_state']) 

    df = pd.read_csv(str(Config.ORIGINAL_DATASET_FILE_PATH))
    # Split data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(df)

    # The predicted column is "quality" which is a scalar from [3, 9]
    X_train = train.drop(["quality"], axis=1)
    X_test = test.drop(["quality"], axis=1)
    y_train = train[["quality"]]
    y_test = test[["quality"]]

    #nahhh how can this be adjusted?
    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run():
        # add variant vor LogistigRegression later
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        (rmse, mae, r2) = eval_metrics(y_test, y_pred)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        # Skipped the part with the model registry as it led to errors and complications regarding configurations,
        # which is not of concern at this stage
        
        mlflow.sklearn.log_model(model, "model")