import numpy as np
import pandas as pd
import yaml
#from urllib.parse import urlparse #we don't need this do we?

from sklearn.model_selection import train_test_split
from config import Config

Config.DATASET_PATH.mkdir(parents=True, exist_ok=True)

with open ("params.yaml", "r") as fd:
    params = yaml.safe_load(fd)

random_state = params['random_state']
np.random.seed(random_state)
df = pd.read_csv(str(Config.ORIGINAL_DATASET_FILE_PATH))

#Split the data into training and test sets. (0.75, 0.25) split.
train, test = train_test_split(df)

train.to_csv(str(Config.DATASET_PATH / "train.csv"), index=None)
test.to_csv(str(Config.DATASET_PATH / "test.csv"), index=None)