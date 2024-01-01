import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import cross_validate
from collections import defaultdict
import pandas as pd
from tqdm import tqdm

import pickle
import os
import json

pwd = os.getcwd()

# Define a function to get top-N recommendations for each user
def get_top_n(predictions, n=10):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def svd_function(user_name):

    # Load the dataset
    user_data = pd.read_csv(r'D:\My Files\Loyalsit\SEM2\Step_presentation\Restaurant recommendation\User_data.csv')

    # Remove the non-numeric entry in the 'User_rating' column
    user_data = user_data[pd.to_numeric(user_data['User_rating'], errors='coerce').notna()]
    user_data['Username_encoded'] = user_data['Username'].astype('category').cat.codes
    user_data['Restaurant_names_encoded'] = user_data['Restaurant_names'].astype('category').cat.codes

    # Reader object to parse the ratings
    reader = Reader(rating_scale=(1, 100))
    # Load the dataset into Surprise's format
    data = Dataset.load_from_df(user_data[['Username_encoded', 'Restaurant_names_encoded', 'User_rating']], reader)

    trainset = data.build_full_trainset()

    #load model
    # Load the entire model   
    model_filename = 'models\svd_model.pkl'
    with open(os.path.join(pwd,model_filename), 'rb') as file:
        algo = pickle.load(file)
    # Map the predictions to each user
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)

    top_n = get_top_n(predictions, n=3)

    # Convert the recommendations back to the original restaurant names
    for uid, user_ratings in top_n.items():
        top_n[uid] = [(user_data[user_data['Restaurant_names_encoded'] == iid]['Restaurant_names'].iloc[0], est) for (iid, est) in user_ratings]


    # Check if the username exists in the 'user_data' DataFrame
    if user_name in user_data['Username'].values:
        # Retrieve the encoded value for the username
        encoded_value = user_data.loc[user_data['Username'] == user_name, 'Username_encoded'].iloc[0]
        print(f"The encoded value for '{user_name}' is: {encoded_value}")
    else:
        print(f"Username '{user_name}' not found in the DataFrame.")

    print('Top 3 recommended restaurants for the first user:', top_n[encoded_value])
    
    recomend = []
    for tup in top_n[encoded_value]:
        tup = list(tup)
        recomend.append(tup[0])

    recommended_restaurants = recomend
    recomend = recommended_restaurants
    restaurant_dicts = [{"name": name} for name in recomend]
    
    # convert list of dictionaries into a json string
    restaurant_json = json.dumps(restaurant_dicts)
    return restaurant_json

svd_function('Try2TravelSustainably')
    





