## General:

This repo contains the code and comparison table on which my blogpost [Comparing Metaflow, MLFlow and DVC]() was build upon.

In /Content you'll find the centerpiece Comparison_table.pdf\* which contains the results based on digging through documentations, tutorials and some experimenting with each tool. 

The /src section contains examples + tutorials which aim to help getting a hands-on feeling for each tool and give a base for (further) comparison.
The same machine-learning-example with unified parameters and metrics is adapted to each tool's requirements.
This helps compare things like code-invasiveness, tracking behavior and setup more directly. 

The repository further contains a simple mlops-env.yml file which can be directly used with conda and lists required packages.

Overall I'd recommend copying each example folder into your preferred playground instead of running things in this repository. 
Each tool generates metadata on its way and debugging is made easier with flatter hierarchies. DVC in particular is happy about an own git repository (despite it also works initialized with the option --subdir) this step avoids unnecessary levels of complexity.

For better comparison I decided to use fix parameters.

Parameters to use, based on the [docs](!https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html) for the model:

learing_rate: 0.1  (Generally between: ]0.0 ..1.0[ -> hypertuning)
random_state: 42

train:
  alpha:   [0.0, 0.5, 1,0]
  l1_rate: [0.0, 0.5, 1.0]


## Structure

```
├── Content
│   ├── Comparison_table.pdf
│   ├── Example.md
│   ├── example_clarify.ipynb
│   └── img
├── README.md
├── mlops-env.yml
└── src
    ├── dvc-example
    ├── metaflow-example
    └── mlflow-example
```

## Content
 Comparison_table.pdf   Table comparing each tool based on different factors
 EXAMPLE.md             Containing additional information about the example itself
 REPORT.md              Contains broad overview, conclusions and next steps
 example_clarify.ipynb  For the curious, contains some clarification about the     behavior

## src

### dvc-example

```
├── dvc-example
│   ├── README.md
│   ├── config.py
│   ├── create_dataset.py
│   ├── create_features.py
│   ├── evaluate_model.py
│   ├── params.yaml
│   ├── train_model.py
│   └── wine-quality.csv
```

config.py:          contains path parameters
other *.py files:   the example split into individual scripts
params.yaml:        file for handling parameters
wine-quality.csv    the dataset

Follow the instructions in README.md 

### metaflow-example
```
├── metaflow-example
│   ├── README.md
│   ├── train.py
│   └── wine-quality.csv
```

train.py            machine learning example
params.yaml:        file for handling parameters
wine-quality.csv    the dataset

In the case of metaflow the main part is about how to structure the code itself. Have a look at the README.md for running the example
and Comparison.pdf for further explanations of the concepts at hand

### mlflow-example
```
── mlflow-example
    ├── MLproject
    ├── README.md
    ├── config.py
    ├── mlruns
    ├── params.yaml
    ├── train.py
    └── wine-quality.csv
```

    MLproject:          MLproject file, which is a text file in YAML syntax containing additional information
    config.py           contains path parameters
    train.py            machine learning example
    mlruns:             artifact store share a directory on the local filesystem — ./mlruns
    params.yaml:        file for handling parameters
    wine-quality.csv    the dataset

Have a look at README.md in each subfolder for further information.


\* I know, pdf's in github aren't elegant, but neither are large tables in markdown ^^

