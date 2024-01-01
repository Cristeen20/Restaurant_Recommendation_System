import numpy as np
from lightfm.data import Dataset

import pickle
import pandas as pd
import os

pwd = os.getcwd()

def light_fm_model(model_filename,user_name):

    df = pd.read_csv(r'D:\My Files\Loyalsit\SEM2\Step_presentation\Restaurant recommendation\User_data.csv')
    df['User_rating'] = pd.to_numeric(df['User_rating'], errors='coerce')
    df.dropna(subset=['User_rating'], inplace=True)

    with open(model_filename, 'rb') as file:
        model = pickle.load(file)
    # Assuming df is your DataFrame containing the provided data
    # You might need to install lightfm: pip install lightfm

    # Create a dataset
    dataset = Dataset()
    dataset.fit(df['Username'], df['Restaurant_names'])

    # Get user and item mappings
    user_mapping, _, item_mapping, _ = dataset.mapping()
    print(len(item_mapping))  

    # Map usernames to indices
    user_id = user_mapping[user_name]  # Replace 'Simon Tremblay' with the target user

    # Map restaurant names to indices for all items
    item_ids = np.array([item_mapping[item] for item in df['Restaurant_names']])
    print(len(item_ids))  
    # Make predictions for the target user
    scores = model.predict(user_id, item_ids)

    # Get the indices of the top 5 recommended items
    top_items = np.argsort(scores)[::-1][:3]

    # Map the indices back to restaurant names
    top_restaurants = [item for item, idx in item_mapping.items() if idx in top_items]

    # Print the top 5 recommended restaurants
    print(f'Top 3 recommended restaurants: {top_restaurants}')

light_fm_model(os.path.join(pwd,'models\lightfm_model.pkl'),'Try2TravelSustainably')