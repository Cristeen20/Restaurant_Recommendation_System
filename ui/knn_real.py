import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

import pickle
import os
import json
pwd = os.getcwd()

def recommend_top_restaurants(username,user_item_matrix, top_n=3):
    try:
        user_index = user_item_matrix.index.get_loc(username)
    except KeyError:
        print(f"User '{username}' not found in the dataset.")
        return pd.Series()  # Return an empty Series if the user is not found

    model_filename = 'models\knn_model.pkl'
    with open(os.path.join(model_filename), 'rb') as file:
        knn_model = pickle.load(file)

    distances, indices = knn_model.kneighbors(user_item_matrix.iloc[user_index, :].values.reshape(1, -1), n_neighbors=top_n+1)
    similar_user_indices = indices.flatten()[1:]  # Exclude the user itself

    # Get the usernames corresponding to the similar user indices
    similar_usernames = user_item_matrix.iloc[similar_user_indices].index

    # Predict ratings for unrated restaurants based on similar users
    unrated_restaurants = user_item_matrix.iloc[user_index, :][user_item_matrix.iloc[user_index, :] == 0].index
    predicted_ratings = user_item_matrix.loc[similar_usernames, unrated_restaurants].mean(axis=0)

    # Sort and recommend the top N restaurants
    top_restaurants = predicted_ratings.sort_values(ascending=False).head(top_n)

    return top_restaurants


def knn_actual(target_username):
    df = pd.read_csv(r'D:\My Files\Loyalsit\SEM2\Step_presentation\Restaurant recommendation\User_data.csv')

    df['User_rating'] = pd.to_numeric(df['User_rating'], errors='coerce')
    df.dropna(subset=['User_rating'], inplace=True)


    duplicate_entries = df[df.duplicated(['Username', 'Restaurant_names'], keep=False)]
    df_no_duplicates = df.drop_duplicates(['Username', 'Restaurant_names'])

    user_item_matrix = df_no_duplicates.pivot(index='Username', columns='Restaurant_names', values='User_rating').fillna(0)
    user_similarity_matrix = cosine_similarity(user_item_matrix)
    recommended_restaurants = recommend_top_restaurants(target_username,user_item_matrix, top_n=3)

    # Print the recommended restaurants
    if not recommended_restaurants.empty:
        print("Top 3 recommended restaurants for user {}: {}".format(target_username, recommended_restaurants.index.tolist()))
        recomend = recommended_restaurants.index.tolist()
        restaurant_dicts = [{"name": name} for name in recomend]

        # convert list of dictionaries into a json string
        restaurant_json = json.dumps(restaurant_dicts)
        print(restaurant_json)
        return restaurant_json

target_username = 'Try2TravelSustainably'  # Replace with the username of the target user
knn_actual(target_username)