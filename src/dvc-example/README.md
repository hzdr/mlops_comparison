
### Preparation:
(Copied from a blogpost I wrote about dvc  along the way)

Go to a project directory of your choice and clone the repository:

`git clone git@github.com:hzdr/dvc_tutorial_series.git`

Switch into the source directory and initialize git and dvc:
```
cd dvc_tutorial_series/src
git init
dvc init
```

Add the remote storage to use (we will stay on our local machine in this case):
```
mkdir /tmp/dvc_demo_test
dvc remote add -d localremote /tmp/dvc_demo_test
dvc remote list
```

>DVC stores information about the added data in a special file named wine-quality.csv.dvc, a small text file with a human-readable format. 
We can version this file like source code with Git, as a placeholder for the original data (which gets listed in `.gitignore`)


Check the content: ([bat](!https://github.com/sharkdp/bat) is just my preferred choice ^^)
```
bat .gitignore
bat wine-quality.csv.dvc
```
Add data to dvc and the placeholder file to git:
```
dvc add wine-quality.csv
git add wine-quality.csv.dvc
```

Add our example code to git (sanity checking is always a good idea):
```
git status
git add .
git commit -m “fresh experiment started”
```

Push data to dvc (local) storage:
```
dvc push
~Output:
  1 file pushed
```

Check output:
```
ls -R /tmp/dvc_demo_test

~Output:
  17
  /tmp/dvc_demo_test/17:
  fbffe83c746612cc247b182e9f7278
```


### Test pipeline

Execute [`dvc run`](!https://dvc.org/doc/command-reference/run)  to create stages. Stages are the unique steps of a pipeline and can be tracked via git.
Stages also connect code to its data input and output (similar to [Snakemake](!https://snakemake.readthedocs.io/en/stable/)).
The stages with all according dependencies and parameters get written to a special [pipeline file named dvc.yaml](!https://dvc.org/doc/user-guide/project-structure/pipelines-files).

I divided the code into different scripts to demonstrate the staging and pipelining process.

---

**Create dataset**
```
dvc run -f -n prepare\
-d create_dataset.py \
-o assets/data \
python create_dataset.py
```

-n the name of the stage

-d dependencies of this stage

-o output of the results

**Featurize**
```
dvc run -f -n featurize \
-d create_features.py \
-d assets/data \
-o assets/features \
python create_features.py
```

..as we can see we have now two dependencies, the feature-creating script and the output of the previous step.

**Train model**
```
dvc run -f -n train \
-d train_model.py \
-d assets/features \
-o assets/models \
-p model_type,random_state,train \
python train_model.py
```

-p use specified parameters from parameters.yaml file

Quick glance into parameters.yaml:
```
model_type: ElasticNet
lr: 0.0041
random_state: 42
train:
  epochs: 70
  alpha: 0.01
  l1_rate: 0.5
```

**Evaluate model**\
```
dvc run -f -n evaluate \
-d evaluate_model.py \
-d assets/features \
-d assets/models \
-p model_type \
-M assets/metrics.json \
python evaluate_model.py
```

-M writes metrics to a specified output destination, in our case mean_squared_error, mean_absolute_error, r2_score


---

Now, lets track our changes:
```
git add assets/.gitignore dvc.yaml dvc.lock
git commit -m “added stages to demo_test”
```

dvc.yaml now includes information about the commands we ran, its dependencies, and outputs.

```
bat dvc.yaml
~Output:
stages:
  prepare:
    cmd: python create_dataset.py
    deps:
    - create_dataset.py
    outs:
    - assets/data
  featurize:
    cmd: python create_features.py
    deps:
    - assets/data
    - create_features.py
    outs:
    - assets/features
  train:
    cmd: python train_model.py
    deps:
    - assets/features
    - train_model.py
    params:
    - model_type
    - random_state
    - train
    outs:
    - assets/models
  evaluate:
    cmd: python evaluate_model.py
    deps:
    - assets/features
    - assets/models
    - evaluate_model.py
    params:
    - model_type
    metrics:
    - assets/metrics.json:
        cache: false
```

There’s no need to use [`dvc add`](!https://dvc.org/doc/command-reference/add) for DVC to track stage outputs, [`dvc run`](!https://dvc.org/doc/command-reference/run#run) already took care of this.
You only need to run [`dvc push`](!https://dvc.org/doc/command-reference/push) if you want to save them to remote storage. (In our case we address our local storage)
```
dvc push
~Output:
  8 files pushed
```

Check dvc push:
`ls -R /tmp/dvc_demo_test`



### Test parameter changes

The whole point of creating the stages and the dvc.yaml file is for being able to reproduce and easily run the pipeline when changes occur.

When executing [`dvc repro`](!https://dvc.org/doc/command-reference/repro) with no change to the codebase or parameters:

..nothing happens.

Now lets open `params.yaml` and change some parameters (e.g alpha from 0.01 to 0.1) and re-run the pipeline.
```
dvc repro
~ Output:
 Stage ‘prepare’ didn’t change, skipping
 Stage ‘featurize’ didn’t change, skipping
 Running stage ‘train’:
   > python train_model.py
 Updating lock file ‘dvc.lock’
 
 To track the changes with git, run:
  git add dvc.lock
 Use `dvc push` to send your updates to the remote storage.
```

Look at the changes between our last commit and the current run:
```
dvc params diff — all

~Output:
 Path Param Old New
 params.yaml lr 0.0041 0.0041
 params.yaml model_type ElasticNet ElasticNet
 params.yaml random_state 42 42
 params.yaml train.alpha 0.01 0.1
 params.yaml train.epochs 70 70
 params.yaml train.l1_rate 0.5 0.5
```

Lets track our changes:
```
git add dvc.lock params.yaml
git commit -m “changed alpha parameter”
```

For the sake of it, we can print the stages as graph by executing dvc dag:
```
+---------+
         | prepare |
         +---------+
              *
              *
              *
        +-----------+
        | featurize |
        +-----------+
         **        **
       **            *
      *               **
+-------+               *
| train |             **
+-------+            *
         **        **
           **    **
             *  *
        +----------+
        | evaluate |
        +----------+
+----------------------+
| wine-quality.csv.dvc |
```

When given appropriate structure, DVC automatically determines which parts of a project need to be re-run. Runs and their results are cached to avoid unnecessary re-runs of stages. (automation)

`dvc.yaml` and `dvc.lock` files describe what data to use and which commands will generate the pipeline results. These files can be versioned and shared via git. (reproducibility)


### Test metric changes

We currently use mean_squared_error (RMSE) and mean_absolute_error (MAE) as metrics

Contents of assets/metrics.json after running the evaluate pipeline:
`{“rmse”: 0.10888875839569741, “mae”: 0.08314237592519587}`

Now lets add r2_score (R2) into our evaluate_model.py script and re-run the stages. Dvc realizes that the script has been tinkered with and re-runs only that one stage:

```
dvc repro
~Output:
 Stage ‘prepare’ didn’t change, skipping
 Stage ‘featurize’ didn’t change, skipping
 Stage ‘train’ didn’t change, skipping
 Running stage ‘evaluate’:
  > python evaluate_model.py
 
Updating lock file ‘dvc.lock’
```

This time, `assets/metrics.json` looks as follows:

`{“rmse”: 0.10888875839569741, “mae”: 0.08314237592519587, “r2”: 0.9829560472003764}`

### Test dataset changes

In the beginning, we created a (local) remote storage and executed dvc push to copy the locally cached data to that storage.
Let’s check if its there:

```
ls -R /tmp/dvc_demo_test
~Output:
 /tmp/dvc_demo_test/17:
 fbffe83c746612cc247b182e9f7278
 /tmp/dvc_demo_test/1a:
 240023ddb507d979001525a8ec2669
..
```

We can see several hashes here, so which one is our actual data?
A look into wine-quality.csv.dvc reveals:

`- md5: 17fbffe83c746612cc247b182e9f7278`

thus the first entry contains our data.

Now lets test how well retrieving works..
First, remove both cache and original data:

```
rm -rf .dvc/cache
rm -f wine-quality.csv
```

Then, get the data from the storage:

```
dvc pull
~Output:
 A wine-quality.csv
 1 file added and 6 files fetched
```

Now lets alter the dataset by adding one additional imaginary bottle at the beginning of wine-quality.csv ..

```
“fixed acidity”,”volatile acidity”,”citric acid”,”residual sugar”,”chlorides”,”free sulfur dioxide”,”total sulfur dioxide”,”density”,”pH”,”sulphates”,”alcohol”,”quality”
7.1,0.28,0.33,19.7,0.046,45,170,1.001,3,0.45,8.8,6 #our fake bottle
7,0.27,0.36,20.7,0.045,45,170,1.001,3,0.45,8.8,6
```

..and add the actual version to the storage:

```
dvc add wine-quality.csv
~Output:
 100% Add|  ████████████████████████████████████████████████████████████████████████████████████████████████████|1/1 [00:08, 8.27s/file]
```

Track the changes with git..

```
git add wine-quality.csv.dvc
git commit -m “updated dataset with fake bottle”
```

..and push the actual version to the storage:

```
dvc push
~Output:
 1 file pushed
```

Oops, we just learned our fake bottle turns out to be vinegar. Let’s roll back to a previous version of our dataset.

First, sanity- check your current state with git log to see where our current HEAD is. 
Then, go one step back to the previous state of the .dvc file:

```
git checkout HEAD~1 wine-quality.csv.dvc
~Output:
 Updated 1 path from cb50800
dvc checkout

~Output:
 M wine-quality.csv
```

Looking into wine-quality.csv, our fake bottle is gone. :)

Don’t forget to commit your changes:

`git commit -m “reverting dataset update"`


## Experiments (WIP)

dvc exp run is similar to dvc repro but with some added conveniences for running experiments. The `--set-param` (or `-S`) flag sets the values for various parameters as a shortcut to editing `params.yaml`.

First, we need to queue some experimets: 

We can define all the combinations we want to try without executing anything, by using the `--queue` flag (like a dry-run): 

```
dvc exp run --queue -S train.alpha=0.1
dvc exp run --queue -S train.alpha=0.01
dvc exp run --queue -S train.alpha=0.05
dvc exp run --queue -S train.alpha=0.5
```

..and now we run them:
`dvc exp run --run-all --jobs 2`

..lets have a look now:
`dvc exp show --no-timestamp --include-params train.alpha`

DVC tracks everything in the pipeline for each experiment (parameters, metrics, dependencies, and outputs) and can later retrieve it as needed

..lets pick one experiment to apply:
`dvc exp apply exp-98a96`


once an experiment has been applied to the workspace, it is no different from reproducing the result without `dvc exp run`
Let's make it persistent in our regular pipeline by committing it in our Git branch:

```
git add dvc.lock dvc.lock params.yaml assets/metrics.json
git commit -m "Preserve example exp-xxx data"
git push
dvc push
```

Cleanup:
```
dvc exp gc --workspace
dvc gc --workspace
```

