
import pandas as pd
from textblob import TextBlob

def trim_data(file_name,column):
    data = pd.read_csv(file_name,encoding='latin1')
    data = data.iloc[1:]

    update_rev = []
    for rv in data[column]:
        try:
            rv = rv.split(" ")[1]
            rv = ''.join(rv)
            rv = rv.split("_")[1]
            print(rv)
            
            
        except:
            print(rv)
        update_rev.append(rv)
    
    data[column] = update_rev
    data.to_csv(file_name, index=False) 

def trim_data_rest(file_name,column):
    data = pd.read_csv(file_name,encoding='latin1')
    data = data.iloc[1:]

    update_rev = []
    for rv in data[column]:
        try:
            rv = rv.split(" ")[0]
            print(rv)
        except:
            print(rv)
        update_rev.append(rv)
    
    data[column] = update_rev
    data.to_csv(file_name, index=False)


def get_sentiment(file_name,column):
    data = pd.read_csv(file_name,encoding='latin1')
    data = data.iloc[1:]

    update_senti = []
    for rv in data[column]:
        try:
            blob = TextBlob(rv)
            sentiment_polarity = blob.sentiment.polarity
            sentiment = "{:.2f}".format(sentiment_polarity)
            update_senti.append(sentiment)
        except Exception as e:
            print(e)
            #update_senti.append(0)
    
    data['Short_Reviews_sentiment'] = update_senti
    
    data.to_csv(file_name, index=False) 

#trim_data("data.csv",'User_rating')
#get_sentiment("data.csv",'Short_Reviews')

#trim_data_rest("Restaurant_data.csv",'Rating')
#trim_data_rest("Restaurant_data.csv",'Review Count')