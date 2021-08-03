import pandas as pd

import yaml
import pickle

from sklearn.linear_model import ElasticNet, LogisticRegression
from config import Config

Config.MODELS_PATH.mkdir(parents=True, exist_ok=True)

with open ("params.yaml", "r") as fd:
    params = yaml.safe_load(fd)

model_type = params['model_type']
model = params['model']
random_state = params['random_state']
#epochs = params['train']['epochs']
alpha = params['train']['alpha']
l1_rate = params['train']['l1_rate']


X_train = pd.read_csv(str(Config.FEATURES_PATH / "train_features.csv"))
y_train = pd.read_csv(str(Config.FEATURES_PATH / "train_labels.csv"))

if model_type == "LogisticRegression":
    model = LogisticRegression(l1_ratio=l1_rate, random_state=random_state)

if model_type == "ElasticNet":
    model = ElasticNet(
        alpha=alpha, l1_ratio=l1_rate, random_state=random_state
        )

model.fit(X_train, y_train)

pickle.dump(model, open(str(Config.MODELS_PATH / "model.pickle"), "wb"))