#!/usr/bin/env python3

# import relevant libraries
from flask import Flask, jsonify, request, render_template
import json
import sys 
from joblib import dump, load
import traceback
import pandas as pd
import numpy as np

#Api Definition 
app = Flask (__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.form.get("predict") == "predict":
        try:
            loaded_model = load("model.pkl")

            sex = request.form.get("sex_male")
            age = request.form.get("age")
            embarked1 = request.form.get("embarked_Q")
            embarked2 = request.form.get("embarked_S")

 # get the form values by referencing the `name` attribute for each input in the form
            data_list = [(sex),(age),(embarked1),(embarked2)]

            #convert list of tuples to an array of appropriate shape and then to a dataframe
            query_df = pd.DataFrame(np.array(data_list).reshape(1,-1))

            #get dummy variables ofthe dataframe 
            dummy_var = pd.get_dummies(query_df)
            



if __name__ == "__main__":
    app.run()
