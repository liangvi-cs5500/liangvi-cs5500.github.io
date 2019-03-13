from flask import Flask
from flask_restful import Resource, Api
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler

import pandas as pd
import numpy as np
import json
import math

app = Flask(__name__)
api = Api(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

@app.route('/roc/<preprocessing>/<c>', methods=['GET'])
def roc(preprocessing, c):
    df = pd.read_csv('data/transfusion.data')
    xDf = df.loc[:, df.columns != 'Donated']
    y = df['Donated']

    # get random numbers to split into train and test
    np.random.seed(1)
    r = np.random.rand(len(df))

    # split into train test
    X_train = xDf[r < 0.8]
    X_test = xDf[r >= 0.8]
    y_train = y[r < 0.8]
    y_test = y[r >= 0.8]

    #Standardization
    scaler = StandardScaler()
    if preprocessing == "standard":
    	scaler = StandardScaler()
    if preprocessing == "normalization":
        scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    #Logistic Regression
    LR = LogisticRegression(C= float(c), random_state=0, solver='lbfgs')
    LR.fit(X_train, y_train)
    probs = LR.predict_proba(X_test)
    fprs, tprs, thresholds = roc_curve(y_test, probs[:,1], pos_label=1)
    score = roc_auc_score(y_test, probs[:,1])

    # Return a list of dictionaries
    dicts = []
    for i in range(len(fprs)):
        dicts.append({"fpr":round(fprs[i], 4),"tpr":round(tprs[i], 4), "threshold": thresholds[i], "score": round(score, 4)})
    return json.dumps(dicts, indent = 4, sort_keys=True)

if __name__ == '__main__':
	# load data
	df = pd.read_csv('data/transfusion.data')
	xDf = df.loc[:, df.columns != 'Donated']
	y = df['Donated']
	# get random numbers to split into train and test
	np.random.seed(1)
	r = np.random.rand(len(df))
	# split into train test
	X_train = xDf[r < 0.8]
	X_test = xDf[r >= 0.8]
	y_train = y[r < 0.8]
	y_test = y[r >= 0.8]
	app.run(debug=True)
