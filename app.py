import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the data into a pandas DataFrame
data = pd.read_csv(r'9eurotweets-sentiment-collocations.csv')

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Set the page title
st.title("Twitter Sentiment Analysis Dashboard")

# Stacked column chart for Sentiment Over Time
st.subheader("Sentiment Over Time")
sentiment_chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('monthdate(Date):T', title='Date'),
    y='count()',
    color='Sentiment',
    tooltip=['monthdate(Date):T', 'count()']
).properties(
    width=800,
    height=400
).interactive()
st.altair_chart(sentiment_chart)

# Function to read the German stopwords file
def read_stopwords():
    stopwords = []
    with open("stopwords-de.txt", "r", encoding="utf-8") as file:
        for line in file:
            stopwords.append(line.strip())
    return stopwords

# Wordcloud for Positive Sentiment
st.subheader("Wordcloud for Positive Sentiment")
positive_tweets = ' '.join(data[data['Sentiment'] == 'positive']['Text'])
wordcloud_positive = WordCloud(background_color='white', stopwords=read_stopwords()).generate(positive_tweets)
plt.imshow(wordcloud_positive, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt.gcf())

# Wordcloud for Negative Sentiment
st.subheader("Wordcloud for Negative Sentiment")
negative_tweets = ' '.join(data[data['Sentiment'] == 'negative']['Text'])
wordcloud_negative = WordCloud(background_color='white', stopwords=read_stopwords()).generate(negative_tweets)
plt.imshow(wordcloud_negative, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt.gcf())

# Wordcloud for Neutral Sentiment
st.subheader("Wordcloud for Neutral Sentiment")
neutral_tweets = ' '.join(data[data['Sentiment'] == 'neutral']['Text'])
wordcloud_neutral = WordCloud(background_color='white', stopwords=read_stopwords()).generate(neutral_tweets)
plt.imshow(wordcloud_neutral, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt.gcf())

# Top-n Tweets with most Engagement
n = st.selectbox("Select the number of top tweets:", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=4)
top_tweets = data.nlargest(n, 'Likes')
st.subheader(f"Top-{n} Tweets with most Engagement")
st.table(top_tweets[['Text', 'Sentiment', 'Likes', 'Replies', 'Retweets']])
