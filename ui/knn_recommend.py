from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
from collections import defaultdict

import pandas as pd
import pickle
import os

pwd = os.getcwd()

def get_top_n(predictions, n=5):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Sort the predictions for each user and retrieve the top N
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def knn_model(username):
    reader = Reader(rating_scale=(1, 100))

    df = pd.read_csv(r'D:\My Files\Loyalsit\SEM2\Step_presentation\Restaurant recommendation\User_data.csv')
    df['User_rating'] = pd.to_numeric(df['User_rating'], errors='coerce')
    df.dropna(subset=['User_rating'], inplace=True)
    data = Dataset.load_from_df(df[['Username', 'Restaurant_names', 'User_rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    model_filename = 'models\knnmodel.pkl'
    with open(os.path.join(model_filename), 'rb') as file:
        model = pickle.load(file)

    predictions = model.test(testset)
    top_n_recommendations = get_top_n(predictions, n=3)
    print(f"Top 5 recommendations for {username}: {top_n_recommendations[username]}")

username = 'Try2TravelSustainably'
knn_model(username)