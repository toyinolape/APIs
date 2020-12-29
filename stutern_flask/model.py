#!/usr/bin/env python3

import pandas as pd
import numpy as np


df = pd.read_csv("titanic.csv")

vars = ["survived","sex","age","embarked"]

titanic = df[vars]

#Fill in the empty Age cells with the average Age on onboard
titanic["age"].fillna(titanic["age"].mean(), inplace=True)

#Fill in the empty Embarked cells with the most occuring embarked value
titanic["embarked"].fillna(titanic["embarked"].value_counts().index[0], inplace=True)

#Encoding the categorical features 
titanic = pd.get_dummies(titanic, columns = ['sex', 'embarked'], drop_first = True)

#Spliting the X & Y variables and spliting test and training datasets 
X = titanic.drop('survived', axis = 1)
y = titanic["survived"]

X_t = X.values
y_t = y.values 

from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression(max_iter = 10000)

# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_t, y_t, test_size = 0.3, random_state=42)

logreg.fit(X_train,y_train)

print("---Model is trained!---")

# saving the model
from joblib import dump, load
dump(logreg, 'model.pkl')

print("---Model dumped!---")

# Save the features columns 

model_cols = list(X.columns)

# save model columns
dump(model_cols, 'model_cols.pkl')
print("---Models columns dumped!---")