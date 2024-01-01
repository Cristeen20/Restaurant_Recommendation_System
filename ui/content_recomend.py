
import numpy as np
import pandas as pd
import json

import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')


from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


def get_restaurant_recommendations(name):

    df = pd.read_csv(r'D:\My Files\Loyalsit\SEM2\Step_presentation\Restaurant recommendation\Restaurant_data.csv')
    df.set_index('Restaurant Name', inplace=True)
    indices = pd.Series(df.index)
    print(df['Review List'])

    # Creating tf-idf matrix
    tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.1,max_df=0.8, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['Review List'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    recommend_restaurant = []

    # Find the index of the hotel entered
    idx = indices[indices == name].index[0]

    # Find the restaurants with a similar cosine-sim value and order them from bigges number
    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)

    # Extract top 30 restaurant indexes with a similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)

    # Names of the top 30 restaurants
    for each in top30_indexes:
        recommend_restaurant.append(list(df.index)[each])

    # Creating the new data set to show similar restaurants
    df_new = pd.DataFrame(columns=['Cusines','Rating'])
    # Create the top 30 similar restaurants with some of their columns
    #for each in recommend_restaurant:
    #    df_new = df_new.concat(pd.DataFrame(df[['Cusines','Rating']][df.index == each].sample()))

    for each in recommend_restaurant:
        sampled_row = df[['Cusines','Rating']][df.index == each].sample()
        df_new = pd.concat([df_new, sampled_row], ignore_index=False)
    
    # Drop the same named restaurants and sort only the top 10 by the highest rating
    df_new = df_new.drop_duplicates(subset=['Cusines','Rating'], keep=False)
    df_new = df_new.sort_values(by='Rating', ascending=False).head(10)

    print('TOP %s RESTAURANTS LIKE %s WITH SIMILAR REVIEWS: ' % (str(len(df_new)), name))
    restaurant_names = df_new.index.tolist()

    restaurant_dicts = [{"name": name} for name in restaurant_names]

    # convert list of dictionaries into a json string
    restaurant_json = json.dumps(restaurant_dicts)
    print(restaurant_json)

    return restaurant_json

#get_restaurant_recommendations('Byblos')