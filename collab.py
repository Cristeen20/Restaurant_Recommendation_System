import pandas as pd
import numpy as np
# Load your CSV file
df = pd.read_csv(r'C:\Users\siva\OneDrive\Desktop\Restaurant Recommendation System\Restaurant_Recommendation_System\User_data.csv')
# Display the first few rows to inspect the data
# print(df.head())

df['User_rating'] = pd.to_numeric(df['User_rating'], errors='coerce')

# Drop rows with missing User_rating
df.dropna(subset=['User_rating'], inplace=True)

# Create user-item matrix
user_item_matrix = df.pivot_table(index='Username', columns='Restaurant_names', values='User_rating', fill_value=0)

# Display the first few rows of the user-item matrix
print(user_item_matrix)

from sklearn.metrics.pairwise import cosine_similarity

# Assuming user_item_matrix is your user-item matrix
user_similarity = cosine_similarity(user_item_matrix)

# Function to predict ratings for a user
def predict_user_ratings(username, user_item_matrix, user_similarity, k=5):
    user_reviews = user_item_matrix.loc[username]
    similar_users = np.argsort(user_similarity[user_item_matrix.index.get_loc(username)])[:-k-1:-1]
    weighted_sum = np.dot(user_similarity[user_item_matrix.index.get_loc(username), similar_users], user_item_matrix.iloc[similar_users])
    normalizing_factor = np.sum(np.abs(user_similarity[user_item_matrix.index.get_loc(username), similar_users]))
    
    if normalizing_factor == 0:
        return np.zeros(user_item_matrix.shape[1])
    
    return weighted_sum / normalizing_factor

# Example usage
username = '284susanl'
predicted_user_ratings = predict_user_ratings(username, user_item_matrix, user_similarity)
print(predicted_user_ratings)
