import numpy as np
import pandas as pd
from io import StringIO #check where we need this

from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from metaflow import FlowSpec, step, IncludeFile, Parameter

def script_path(filename):
    """
    A convenience function to get the absolute path to a file in this
    tutorial's directory. This allows the tutorial to be launched from any
    directory.
    """
    import os

    filepath = os.path.join(os.path.dirname(__file__))
    return os.path.join(filepath, filename)


class WineQualityFlow(FlowSpec):
    """
    A flow to estimate wine quality using sklearns elasticnet
    """
    wine_data = IncludeFile("wine_data",
                             help="path to wine quality data.",
                             default=script_path('wine-quality.csv'))
    
    model_type = Parameter("model_type", 
                            help="model type add help",
                            default="ElasticNet")
    
    random_state = Parameter("random_state",
                              help = "random state add description",
                              default=42)

    alpha = Parameter("alpha",
                      help="alpha add description",
                      default=0.5)
    
    l1_ratio = Parameter("l1_ratio",
                      help="l1 add description",
                      default=0.5)

    @step
    def start(self):
        # Load the data set into a pandas dataframe.
        # aequivalent to create_dataset() in dvc example
        self.dataframe = pd.read_csv(StringIO(self.wine_data))

        self.next(self.create_features)

    @step
    def create_features(self):
        train, test = train_test_split(self.dataframe)
        # The predicted column is "quality" which is a scalar from [3, 9]
        self.X_train = train.drop(["quality"], axis=1)
        self.X_test = test.drop(["quality"], axis=1)
        self.y_train = train[["quality"]]
        self.y_test = test[["quality"]]

        self.next(self.train_model)


    @step
    def train_model(self):
        if self.model_type == "ElasticNet":
            self.model = ElasticNet(alpha=self.alpha, l1_ratio=self.l1_ratio, random_state=self.random_state)

        # place for other models

        self.model.fit(self.X_train, self.y_train)
       
        self.next(self.predict_model)

    @step
    def predict_model(self):
        self.predicted_qualities = self.model.predict(self.X_test)
        self.rmse = np.sqrt(mean_squared_error(self.y_test, self.predicted_qualities))
        self.mae = mean_absolute_error(self.y_test, self.predicted_qualities)
        self.r2 = r2_score(self.y_test, self.predicted_qualities)

        self.next(self.end)

    @step
    def end(self):
        """
        End the flow.
        """
        print(f"Elasticnet model (alpha={self.alpha}, l1_ratio={self.l1_ratio})")
        print(f"RMSE: {self.rmse}")
        print("  MAE: {self.mae}")
        

if __name__ == '__main__':
    WineQualityFlow()