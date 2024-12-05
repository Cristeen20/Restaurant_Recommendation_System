#!/usr/bin/env python
import pandas as pd
import re
import csv

# Load your CSV file into a DataFrame
df = pd.read_csv('restaurant_data.csv')

# Display the first few rows of the DataFrame
df.head()

#unique_address = df['Address'].str.split(', ').explode().unique()
#result = [s for s in unique_address if s and s[0].isdigit()]
#result_without_numbers = [s.lstrip('0123456789') for s in result]
#print(result_without_numbers)
#Fetching the Locations from the Address column
location =[]
for data in df['Address']:
    if(data !='null'):
        parts = data.split(',')
        if(parts[-2] !='null'):
            location.append(parts[-2])
        else:
            location.append('Ontario')
    else:
        location.append('Ontario')
#print(len(location))

df['Location'] = location
# Replace with your desired output file name
output_file = 'Updated_Restaurant_data.csv'
df.to_csv(output_file, index=False)



