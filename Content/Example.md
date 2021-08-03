This document contains notes and some information about the  ML-example I chose to use for this series. (Please feel free to correct me if I got something wrong)

The original code is to be found [here](!https://www.mlflow.org/docs/latest/tutorials-and-examples/tutorial.html)

**wine-quality.csv**
- contains multiple features
- 12 columns, last one is quality and used as label

### OUR SETUP

Parameters to use:
(See the [docs](!https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html))

learing_rate: 0.1    (Generally between: ]0.0 ..1.0[ -> hypertuning)
random_state: 42

train:
  alpha:   [0.0, 0.5, 1,0]
  l1_rate: [0.0, 0.5, 1.0]


### GENERAL INFO

**ElasticNet**
- not actually a model but a regularizator

Regularization:
- has the goal to reduce interpolation
	- interpolation is the fatal case of overfitting, means, your function  basically runs trought every datapoint
- introduces a regulation term (controlled by parameters) which makes extreme differences in w (weights) (wich can be responsible for interpolation) less likely
- different regularizations like 
	- [Ridge](!https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression)
	- [Lasso](!https://scikit-learn.org/stable/modules/linear_model.html#lasso)
	- ..which both have slighly different goals
	
[ElasticNet](!https://scikit-learn.org/stable/modules/linear_model.html#elastic-net) combines two regularization types and is useful in cases of multiple features which are correlated with one another. Paramters:
	- alpha 
	- l1-ratio

**alpha** denotes the strength of the regularization itself whereas **l1_ratio** determines how much of each regularization type is considered (imagine it a bit like a slider)

### Idea:
`ElasticNet` with `alpha = 0` and `l1_ratio = None` --> no regularization should at all. This means instead of trying different model arcitectures one can use a plain ElasticNet as base line and then add parameters.

**RMSE**
- Root Mean Squared Error
- RMSE can be thought of as some kind of (normalized) distance between the vector of predicted values and the vector of observed values.
- measure of the average deviation of the estimates from the observed values
- Serves as a heuristic for training models
- Evaluates trained models for usefulness / accuracy
- **What does it mean for RMSE to be “small”?**:
-  we care about _relative_ size of the error from one step to the next, not the absolute size of the error.
-  we care about units, because we aren’t just trying to see if we’re doing better than last time: we want to know if our model can actually help us solve a practical problem - dependant on problem to solve
-  Question to ask instead:  “What is the probability the RMSE of our trained model on such-and-such set of observations would be this small by random chance?”

**MAE**
- Mean Absolute Error
- summarizes and assesses quality of a machine learning model.
- results of measuring the difference between two continuous variables
- model evaluation metric often used with regression models

**R2**
- root squared error
-  R2 is the fraction of the total sum of squares that is 'explained by' the regression
-  scaled between 0,1