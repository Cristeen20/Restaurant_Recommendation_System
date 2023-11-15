#!/usr/bin/env python
# coding: utf-8

# In[75]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Sample data (assuming the data is loaded into a pandas DataFrame called 'restaurants_df')
restaurants_df =  pd.read_csv('Updated_Restaurant_data.csv')

# Concatenate relevant text data for the TF-IDF vectorization
restaurants_df['Features'] = restaurants_df['Cusines'].apply(lambda x: ' '.join(x)) + ' ' + restaurants_df['Location']

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(restaurants_df['Features'])

# Calculate cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def recommend_restaurants(location, cosine_sim=cosine_sim, df=restaurants_df):
    # Get the index of restaurants in the specified location
    n_d =[]   
    for i in df['Location']:
        i= i.strip()
        if(i==location):
            n_d.append(True)
        else:
            n_d.append(False)
    n_df = pd.DataFrame(n_d)
    
    indices = df[n_df].index.tolist()

    # Calculate similarity scores for restaurants in that location
    sim_scores = list(enumerate(cosine_sim[indices]))

    # Sort restaurants based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1][0], reverse=True)

    # Get the top recommendations (excluding the selected restaurant itself)
    top_recommendations = sim_scores[0:10]  # Change '6' for more recommendations if needed

    # Return the indices of recommended restaurants
    return [df.iloc[idx[0]]['Restaurant Name'] for idx in top_recommendations]

# Example: Get top restaurant recommendations for 'Toronto'
recommended_restaurants = recommend_restaurants('Toronto')
print(recommended_restaurants)


# In[ ]:




