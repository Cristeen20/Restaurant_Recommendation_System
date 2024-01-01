from content_recomend import get_restaurant_recommendations


from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import json

from knn_real import knn_actual
from svd_recommend import svd_function


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
        #if request.method == 'POST':
             #user_input = request.form['user_input']
        return render_template('index.html')
    
@app.route('/recommend/<user_name>', methods=['GET', 'POST'])
def recommend(user_name):
    print("reach recommend")
    print(user_name)

    #if request.method == 'POST':

        # Get the restaurant recommendations
    recommended_restaurants = get_restaurant_recommendations(user_name)
    print(recommended_restaurants)

        # Return the restaurant recommendations as a list of dictionaries
        # (e.g., {'name': 'Restaurant 1', 'address': '123 Street, City'})
    return json.loads(recommended_restaurants)


@app.route('/knn/<user_name>', methods=['GET', 'POST'])
def recommend_knn(user_name):
    print("reach recommend")
    print(user_name)

    #if request.method == 'POST':

        # Get the restaurant recommendations
    recommended_restaurants = knn_actual(user_name)
    print("api")
    print(json.loads(recommended_restaurants))

        # Return the restaurant recommendations as a list of dictionaries
        # (e.g., {'name': 'Restaurant 1', 'address': '123 Street, City'})
    return json.loads(recommended_restaurants)

@app.route('/svd/<user_name>', methods=['GET', 'POST'])
def recommend_svd(user_name):
    print("reach recommend")
    print(user_name)

    #if request.method == 'POST':

        # Get the restaurant recommendations
    recommended_restaurants = svd_function(user_name)
    print(recommended_restaurants)

        # Return the restaurant recommendations as a list of dictionaries
        # (e.g., {'name': 'Restaurant 1', 'address': '123 Street, City'})
    return json.loads(recommended_restaurants)



if __name__ == '__main__':
    app.run(debug=True)