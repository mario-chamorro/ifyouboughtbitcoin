import pandas as pd
from datetime import *
import random
from credentials import *
import tweepy
import urllib
import json

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Generate main DataFrame from csv
# BTC price source: https://www.coindesk.com/price/

df = pd.read_csv("btcprice_fixed.csv", parse_dates = True, index_col = "Date")
df.drop(df.tail(2).index, inplace = True) # delete last 2 unrelevant rows from coindesk csv
df.index = pd.to_datetime(df.index)
df.tail(2)

# Get a ramdom date between the end date and BTC first quoted price (2010-07-18)

investments = [100, 500, 1000, 5000, 10000]

start = datetime(2010, 7, 18)
end = datetime(2018, 5, 31)
investment = random.choice(investments)

random_date = start + (end - start) * random.random()
random_date = random_date.replace(hour=0, minute=0, second=0, microsecond=0)

# Get today bitcoin price through coinmarketcap API
url = "https://api.coinmarketcap.com/v2/ticker/?convert=BTC&limit=10"
json_obj = urllib.request.urlopen(url).readall().decode("utf-8")
data = json.loads(json_obj)
price_today = int(data["data"]["1"]["quotes"]["USD"]["price"])

# Prepare tweet message
end = str(end.replace(hour=0, minute=0, second=0, microsecond=0))
end = str(end[0:10])
price_ramdom_date = df.loc[random_date,:].values[0]
price_ramdom_date = df.loc[random_date,:].values[0]
roi = (price_today / price_ramdom_date)
fortune = "{0:,.0f}".format(investment * roi)
random_date_fixed = str(random_date)[0:10]
investment_formated = str("{0:,.0f}".format(investment))
prince_random_date_formatted = str("{0:,.0f}".format(price_ramdom_date))
message = str("If you bought bitcoin worth $" + str(investment_formated) +
              " in " + str(random_date_fixed) + " you would have $"
              + str(fortune) + " today. BTC price was $" + str(price_ramdom_date) + " at that date!")
print(message)

# Publish tweet
api.update_status(message)
