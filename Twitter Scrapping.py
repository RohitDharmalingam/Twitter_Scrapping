#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
import datetime
from datetime import date
import time


st.header("""
TWITTER SCRAPING - GUVI PROJECT
""")

today=date.today()
search = st.text_input('Enter the Search Term')
count = st.slider('Slide the limit',10,1000)
start_date=st.date_input('Pick start date',datetime.date(2022, 1, 1))
end_date=st.date_input('Pick end date',today)



count = int(count)
submit_button = st.button(label='Search')

tweets_list1 = []

if submit_button:
    for i , tweet in enumerate(sntwitter.TwitterSearchScraper(f'{search} since:{start_date} until:{end_date}').get_items()):
        if i > count-1:
            break
        tweets_list1.append(
            [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount,
             tweet.sourceLabel, tweet.user.location])
tweet_df = pd.DataFrame(tweets_list1, columns=["Date", "Id", "Content", "Username", "LikeCount", "RetweetCount",
                                                       "SourceLabel", "Location"],index=None)

st.dataframe(tweet_df,)

file_converted = tweet_df.to_csv()
st.download_button(
            label="Download data as CSV",
            data=file_converted,
            file_name='twits.csv',
            mime='text/csv',
        )
file_converted = tweet_df.to_json()
st.download_button(
            label="Download data as json",
            data=file_converted,
            file_name='twits.json',
            mime="application/json",
        )
export_button = st.button(label="export")
now = datetime.datetime.now()
client = pymongo.MongoClient("mongodb+srv://bhaarani:bharani09@cluster0.99c2qfp.mongodb.net/?retryWrites=true&w=majority")
db = client.Twitterdata
records = db.search
for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(f'{search} since:{start_date} until:{end_date}').get_items()):
    if i > count :
        break
    tweets_list1.append(
                [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount,
                 tweet.sourceLabel, tweet.user.location])
    tweet_df = pd.DataFrame(tweets_list1,
                                    columns=["Date", "Id", "Content", "Username", "LikeCount", "RetweetCount",
                                             "SourceLabel", "Location"], index=None)
    l = {"Scraped_Name": "search", "Time": now, "Scraped_data": [
                    {"Date_Time": tweet.date, "Tweet_ID": tweet.id, "Tweet_content": tweet.content,
                     "Username": tweet.user.username,
                     "Like Count": tweet.likeCount, "ReTweet Count": tweet.retweetCount, "Source": tweet.sourceLabel,
                     "Location": tweet.user.location}]}
    records.insert_one(l)
if export_button:

    st.balloons()

