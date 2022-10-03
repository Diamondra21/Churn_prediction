# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import flask
from flask import Flask, render_template, request
import pickle
from flask_ngrok import run_with_ngrok
# Running the flask app
app = Flask(__name__)
run_with_ngrok(app)
#load model using pickle
model = pickle.load(open('model.pkl', 'rb'))['model']

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    val_features = [x for x in request.form.values()]
    print(val_features)
    int_features = val_features[:len(val_features)-2]
    print(int_features)
    if 'Spain' in val_features :
        int_features.extend([0,0,1])
    elif 'Germany' in val_features :
        int_features.extend([0,1,0])
    else :
        int_features.extend([1,0,0])
    
    if 'Male' in val_features :
        int_features.extend([0,1])
    else :
        int_features.extend([1,0])
    
    int_features = [int(x) for x in int_features]
    print(int_features)
    prediction = model.predict_proba([int_features])[0][1]
    print(model.predict([int_features]))
    return render_template('index.html', prediction_text='The probability to churn for this customer is {}'.format(prediction))

if __name__ == '__main__':
    app.run()