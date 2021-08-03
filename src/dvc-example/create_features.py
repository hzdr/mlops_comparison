import pandas as pd
from config import Config

Config.FEATURES_PATH.mkdir(parents=True, exist_ok=True)

train = pd.read_csv(str(Config.DATASET_PATH / "train.csv"))
test = pd.read_csv(str(Config.DATASET_PATH / "test.csv"))

#fix redundancy
#train['goodquality'] = [1 if x >= 7 else 0 for x in train['quality']]# Separate feature variables and target variable
#test['goodquality'] = [1 if x >= 7 else 0 for x in test['quality']]# Separate feature variables and target variable

def extract_features(df):
    df["quality"] = df.drop(["quality"], axis=1)
    return df[["quality"]]
    #df["goodquality"] = df.drop(["quality", "goodquality"], axis=1)
    #return df[["goodquality"]] 

def extract_labels(df):
    return df[["quality"]]
    #return df[["goodquality"]]

train_features = extract_features(train)
test_features = extract_features(test)

train_labels = extract_labels(train)
test_labels = extract_labels(test)

train_features.to_csv(str(Config.FEATURES_PATH / "train_features.csv"), index=None)
test_features.to_csv(str(Config.FEATURES_PATH / "test_features.csv"), index=None)

train_labels.to_csv(str(Config.FEATURES_PATH / "train_labels.csv"), index=None)
test_labels.to_csv(str(Config.FEATURES_PATH / "test_labels.csv"), index=None)