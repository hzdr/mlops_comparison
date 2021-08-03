## mlflow test case
This example orginates from https://mlflow.org/docs/latest/tutorials-and-examples/tutorial.html
and is adapted to the metaflow programming paradigm

Contents of example:
* Train a linear regression model
* Package the code that trains the model in a reusable and reproducible model format
* Deploy the model into a simple HTTP server that will enable you to score predictions
* This tutorial uses a dataset to predict the quality of wine based on quantitative features like the wine’s “fixed acidity”, “pH”, “residual sugar”, and so on

The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.
This example code



### Preparation
In order to work with metaflow we first need to transform our example into a fitting form, which is the main part of the work. 

Have a look into src/metaflow-example/train.py to see how the adjusted and commented example looks like.
For further information about the code-structure itself, please read [here](!https://docs.metaflow.org/metaflow/basics)

Informations about the example itself can be found in `Content/EXAMPLE.md`

### Notes

We have a _start_ and and _end_ step within a FlowSpec class. 
Steps are changed together via iterators instead of return statements

```
class WineQualityFlow(FlowSpec):
...
    @step
    def start(self):
        self.dataframe = pd.read_csv(StringIO(self.wine_data))
        self.next(self.create_features)

    ...

    @step
    def end(self):
        """
        End the flow.
        """
        print(f"Elasticnet model (alpha={self.alpha}, l1_ratio={self.l1_ratio})")
        print(f"RMSE: {self.rmse}")
        print("  MAE: {self.mae}")
    
```

Everything is then executed as one single Flow:

```
if __name__ == '__main__':
    WineQualityFlow()
```


### Run example
We first display what _would_ be executed. Below we can see the steps of our flow graph.

`$python train.py show`

Output:

```
Metaflow 2.0.5 executing WineQualityFlow for user:nea

A flow to estimate wine quality using sklearns elasticnet

Step start
    ?
    => create_features

Step create_features
    ?
    => train_model

Step train_model
    ?
    => predict_model

Step predict_model
    ?
    => end

Step end
    End the flow.
```

Now, lets run it:
`python train.py run`

Output:
```
Metaflow 2.0.5 executing WineQualityFlow for user:nea
Validating your flow...
    The graph looks good!
Running pylint...
    Pylint not found, so extra checks are disabled.
2021-06-25 15:21:45.875 Including file /Users/nea/WORK/ml_ops_exploration/src/metaflow-example/wine-quality.csv of size 258KB
2021-06-25 15:21:45.879 Workflow starting (run-id 1624627305871250):
2021-06-25 15:21:45.884 [1624627305871250/start/1 (pid 12729)] Task is starting.
2021-06-25 15:21:46.773 [1624627305871250/start/1 (pid 12729)] Task finished successfully.
2021-06-25 15:21:46.779 [1624627305871250/create_features/2 (pid 12732)] Task is starting.
2021-06-25 15:21:47.750 [1624627305871250/create_features/2 (pid 12732)] Task finished successfully.
2021-06-25 15:21:47.757 [1624627305871250/train_model/3 (pid 12737)] Task is starting.
2021-06-25 15:21:48.724 [1624627305871250/train_model/3 (pid 12737)] Task finished successfully.
2021-06-25 15:21:48.731 [1624627305871250/predict_model/4 (pid 12741)] Task is starting.
2021-06-25 15:21:49.697 [1624627305871250/predict_model/4 (pid 12741)] Task finished successfully.
2021-06-25 15:21:49.703 [1624627305871250/end/5 (pid 12745)] Task is starting.
2021-06-25 15:21:50.540 [1624627305871250/end/5 (pid 12745)] Elasticnet model (alpha=0.5, l1_ratio=0.5)
2021-06-25 15:21:50.653 [1624627305871250/end/5 (pid 12745)] RMSE: 0.8476463170247194
2021-06-25 15:21:50.653 [1624627305871250/end/5 (pid 12745)] MAE: {self.mae}
2021-06-25 15:21:50.656 [1624627305871250/end/5 (pid 12745)] Task finished successfully.
2021-06-25 15:21:50.656 Done!
```

