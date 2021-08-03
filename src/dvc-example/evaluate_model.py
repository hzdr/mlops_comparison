import numpy as np
import pandas as pd

import pickle
import json
import yaml

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from config import Config


with open ("params.yaml", "r") as fd:
    params = yaml.safe_load(fd)

model_type = params['model_type']
alpha = params['train']['alpha']
l1_rate = params['train']['l1_rate']

X_test = pd.read_csv(str(Config.FEATURES_PATH / "test_features.csv"))
y_test = pd.read_csv(str(Config.FEATURES_PATH / "test_labels.csv"))

model = pickle.load(open(str(Config.MODELS_PATH / "model.pickle"), "rb"))

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
#r2 = r2_score(y_test, y_pred)


#print(f"RMSE : {rmse}\nMAE : {mae}\nR2 : {r2}")

#For dvc we just write this out as regular data and track it later
with open(str(Config.METRICS_FILE_PATH), "w") as outfile:
    json.dump(dict(rmse=rmse, mae=mae), outfile)
