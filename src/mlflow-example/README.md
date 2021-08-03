##mlflow test case
This example orginates from https://mlflow.org/docs/latest/tutorials-and-examples/tutorial.html


* Train a linear regression model
* Package the code that trains the model in a reusable and reproducible model format
* Deploy the model into a simple HTTP server that will enable you to score predictions
* This tutorial uses a dataset to predict the quality of wine based on quantitative features like the wine’s “fixed acidity”, “pH”, “residual sugar”, and so on

The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.


### Notes

The example we use here is the original mlflow example found [here](!https://www.mlflow.org/docs/latest/tutorials-and-examples/tutorial.html)

Look either directly there or in `src/mlflow-example/train.py` 
in order to see how the code must be written in order to work with MLflow:

```
mlflow.set_tracking_uri("http://localhost:5000")
...

...

mlflow.log_param("alpha", alpha)
mlflow.log_param("l1_ratio", l1_ratio)
mlflow.log_metric("rmse", rmse)
mlflow.log_metric("r2", r2)
mlflow.log_metric("mae", mae)
```
The [MLflow tracking APIs](https://www.mlflow.org/docs/latest/tracking.html) logs information about each training run, which includes hyperparameters `alpha` and `l1_ratio` and the metrics `rmse`, `r2` and `mae`. 


The part with the model registry from the original example was removed as it led to errors in accessing the Tracking UI 
(some additional configuration work must be taken into account which is currently beyond the scope of this example)


```
if tracking_url_type_store != "file":
	mlflow.sklearn.log_model(model, "model", 	registered_model_name="ElasticnetWineModel")
else:
	mlflow.sklearn.log_model(model, "model")
```

By default, wherever you run your program, the tracking API writes data into files into a local ./mlruns directory. 

### Run example

If you first execute train.py, you can run into following issue:

```
File "/Users/nea/miniconda3/envs/mlops-env/lib/python3.9/site-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=5000): Max retries exceeded with url: /api/2.0/mlflow/runs/create (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x179604ca0>: Failed to establish a new connection: [Errno 61] Connection refused'))
```

Instead, first start the ui (or train.py will fail, which is an unecpected behavior)

`mlflow ui`

..and then execute the script:

`python train.py`

Output:
```
Elasticnet model (alpha=0.500000, l1_ratio=0.500000):
  RMSE: 0.821195103195106
  MAE: 0.6338934920844772
  R2: 0.1313572669551294
```

You can view the UI in your browser at http://localhost:5000. You can also configure a [remote tracking server](!https://www.mlflow.org/docs/latest/tracking.html#tracking-server) and [log to it](!https://www.mlflow.org/docs/latest/tracking.html#logging-to-a-tracking-server)


![mlflow GUI 00](/Content/img/mlflow_00.png)

![mlflow GUI 01](/Content/img/mlflow_01.png)


MLflow allows you to package code and its dependencies as a project that can be run in a reproducible fashion on other data. Each project includes its code and a MLproject file that defines its dependencies (for example, Python environment) as well as what commands can be run into the project and what arguments they take.

You can easily run existing projects with the mlflow run command, which runs a project from either a local directory or a GitHub URI:

Cd into `src/` and execute following command:
(--no-conda specified as we already use conda)

`mlflow run mlflow-example --no-conda`

It can happen that one runs into following error:
```
..
mlflow.exceptions.RestException: RESOURCE_DOES_NOT_EXIST: Run '76f0151114c74320bf5289f760de9497' not found
2021/06/25 16:46:53 ERROR mlflow.cli: === Run (ID '76f0151114c74320bf5289f760de9497') failed ===
mlflow.exceptions.RestException: RESOURCE_DOES_NOT_EXIST:
```

..which is also sth that needs to be addressed via debugging configuration settings as stated in this issue [issue](!https://github.com/mlflow/mlflow/issues/1703)

(..starting it from the directory finely connects to the UI)


#### Serve model

When you run the example, it outputs an MLflow run ID for that experiment. If you look at mlflow ui, you will also see that the run saved a model folder containing an MLmodel description file and a pickled scikit-learn model. You can pass the run ID and the path of the model within the artifacts directory (here “model”) to various tools. For example, MLflow includes a simple REST server for python-based models:
(--port 1234 as port 5000 is already in use by our UI)

`mlflow models serve -m runs:/48547f39f945497c9171b49dfb84181b/model --port 1234`

Output:
```
2021/06/25 16:56:08 INFO mlflow.models.cli: Selected backend for flavor 'python_function'
2021/06/25 16:56:09 INFO mlflow.pyfunc.backend: === Running command 'source /Users/nea/miniconda3/bin/../etc/profile.d/conda.sh && conda activate mlflow-6e49d9ffbd688bdca9abb009cf5563483f264729 1>&2 && gunicorn --timeout=60 -b 127.0.0.1:1234 -w 1 ${GUNICORN_CMD_ARGS} -- mlflow.pyfunc.scoring_server.wsgi:app'
[2021-06-25 16:56:09 +0200] [15483] [INFO] Starting gunicorn 20.0.4
[2021-06-25 16:56:09 +0200] [15483] [INFO] Listening at: http://127.0.0.1:1234 (15483)
[2021-06-25 16:56:09 +0200] [15483] [INFO] Using worker: sync
[2021-06-25 16:56:09 +0200] [15484] [INFO] Booting worker with pid: 15484
...
```

Once the server runs, you can pass it some sample data (eg. via [curl](!https://wiki.ubuntuusers.de/cURL/)).For more information about the input data formats accepted by the pyfunc model server, see the [MLflow deployment tools docs](!https://www.mlflow.org/docs/latest/models.html#local-model-deployment).

Type `mlflow models --help` and look at [MLflow Models](!https://www.mlflow.org/docs/latest/models.html) for more information.

TODO: See what else to add