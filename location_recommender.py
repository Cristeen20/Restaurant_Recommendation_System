#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Assuming 'df' contains your restaurant data
df =  pd.read_csv('Updated_Restaurant_data.csv')

# Function to recommend top 10 restaurants based on location
def recommend_restaurants(location):
    # Filter restaurants for the specific location
    df['Location'] = df['Location'].str.strip().str.lower()
    location_restaurants = df[df['Location'] == location]
    #print(location_restaurants)
    #print("Printing the df['Location'] column count: ")
    #print(df['Location'].value_counts())

    # Sort by ratings in descending order
    top_restaurants = location_restaurants.sort_values(by='Rating', ascending=False).head(10)

    return top_restaurants[['Restaurant Name', 'Rating', 'Location']]

# Get top 10 restaurants in Toronto
top_toronto_restaurants = recommend_restaurants('markham')
print(top_toronto_restaurants)


# In[ ]:




