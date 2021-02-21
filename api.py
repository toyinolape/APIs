# import relevant libraries
from flask import Flask, jsonify, request, render_template, url_for
import json
import sys 
from joblib import dump, load
import traceback
import pandas as pd
import numpy as np

# api definition
app = Flask(__name__)

@app.route('/')
def display_form():
    return render_template('./index.html')
    

# define the predict function
@app.route('/predict', methods= ['POST']) # endpoint url will contain /predict
def predict():

    if loaded_model:
        try:

            # get the form values by referencing the `name` attribute for each input in the form
            pclass = request.form.get('Pclass')
            sex = request.form.get('Sex_male')
            age = request.form.get('Age')
            fare = request.form.get('Fare')
            embarked = request.form.get('Embarked_Q')
            embarked2 = request.form.get('Embarked_S')


            # get all input values from form as a list of tuples
            data_dict = [
                        (pclass), (sex),
                        (age), (fare),
                        (embarked), (embarked2)
                        ]

            # convert list of tuples to an array of appropriate shape and then to a dataframe
            query_df = pd.DataFrame(np.array(data_dict).reshape(1, -1))

            # get the dummy variables of the dataframe
            dummy_var = pd.get_dummies(query_df)
        
            # make sure the columns of the data to be predicted are in line with the columns of the trained dataset,
            # if the columns are smaller than expected, fill the excess columns with zeros
            dummy_df = dummy_var.reindex(columns = model_columns, fill_value = 0)

            # predict the survivors
            prediction = ['Survived' if loaded_model.predict(dummy_df) == 1 else 'Died']

            
            # return jsonify({'prediction': str(prediction)})
            return render_template("result.html" , prediction = prediction)

        except: # if model is not loaded, return a traceback

            return jsonify({'trace': traceback.format_exc()})

    else:

        print('Train the model first')

        return ('No model loaded')

@app.route('/train_api', methods = ['GET'])
def train_api():

    exec(open("./model.py").read())

    return "<h1> Training model... </h1><h2> Model Trained </h2>"

# function that prints the statistics of the model
@app.route("/head", methods = ['POST', 'GET'])
def head():
    df = pd.read_csv('http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv')
    return df.head().to_html()

@app.route("/tail", methods = ['POST', 'GET'])
def tail():
    df = pd.read_csv('http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv')
    return df.tail().to_html()


@app.route("/describe", methods = ['POST', 'GET'])
def describe():
    df = pd.read_csv('http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv')
    return df.describe().to_html()

    
# if  __name__ == "__main__":
#     app.run()

# write the main function
if __name__ == '__main__':

    try:
        port = int(sys.argv[1]) # incase a command line port argument is specified use it as default port

    except:

        port = 5200 # if not use this

    loaded_model = load('model.pkl') # load model and assign to variable
    print('model loaded')
    model_columns = load('model_columns.pkl') # load model columns and assign to variable
    print('model columns loaded')
    print(sys.argv)
    app.run(port = port, debug = True)
    