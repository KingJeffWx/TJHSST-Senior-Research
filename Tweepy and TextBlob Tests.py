import pip
import re
import tweepy
import csv
from textblob import *
from textblob.sentiments import NaiveBayesAnalyzer

"""
References:
https://www.programmableweb.com/api/twitter
https://twittercommunity.com/t/how-to-use-the-tweepys-search-api/22105
http://docs.tweepy.org/en/v3.5.0/api.html
http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html
https://gist.github.com/dev-techmoe/ef676cdd03ac47ac503e856282077bf2
https://marcobonzanini.com/2015/04/01/mining-twitter-data-with-python-part-5-data-visualisation-basics/
http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
"""

#Use for installing modules using pip
#pip.main(["install", "tweet-preprocessor"])


consumer_key = 'ihCD9dqB3uXo4I6nRij66Sw1N'
consumer_secret = 'X8SxLBoZAFUJFCkkOWT0ufAr1Wk18ZLZetmdrp7EHbi8DDHZTe'
access_token = 	'4497807209-phRIK2UPwsfAcBZhRtSijf7zIrMZVdwroxXegyl'
access_token_secret = '4FXARctdSjFtN4rGAcXOdeCVCXMyjXKx2iqrl2HOftjzi'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

"""
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

user = api.get_user('twitter')
print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
   print(friend.screen_name)
"""

def get_user_timeline(username, number):
   tweets = api.user_timeline(screen_name=username, count=number)
   text_list = list()
   lang_list = list()
   date_list = list()
   username_list = list()
   retweets_list = list()
   likes_list = list()
   for tweet in tweets:
      text_list.append(tweet.text.encode('utf8'))
      lang_list.append(tweet.lang)
      date_list.append(tweet.created_at)
      username_list.append(tweet.user)
      retweets_list.append(tweet.retweet_count)
      likes_list.append(tweet.favorite_count)
   #for i in range(len(text_list)):
      #print(text_list[i])
   return text_list

def get_user_info(username):
   user = api.get_user(screen_name=username)
   followers = user.followers_count
   tweets = user.statuses_count
   print(followers, tweets)

def get_followers():
   followers = tweepy.Cursor(api.followers, screen_name="@KingJeffWx").items()
   for follower in followers:
      print(follower.screen_name)
      
# https://stackoverflow.com/questions/42994626/tweet-extraction-using-tweepy-with-specific-fields-required
# https://stackoverflow.com/questions/38872195/tweepy-exclude-retweets
def search(query, max_tweets, retweets):
   if not retweets:
      query += " -filter:retweets"
   tweets = tweepy.Cursor(api.search, q=query, lang="en").items(max_tweets)
   i = 1
   text_list = list()
   lang_list = list()
   date_list = list()
   username_list = list()
   retweets_list = list()
   likes_list = list()
   for tweet in tweets:
      text_list.append(tweet.text.encode('utf8'))
      lang_list.append(tweet.lang)
      date_list.append(tweet.created_at)
      username_list.append(tweet.user)
      retweets_list.append(tweet.retweet_count)
      likes_list.append(tweet.favorite_count)
   #for i in range(len(text_list)):
      #print(text_list[i], date_list[i])
   return text_list
      

# https://stackoverflow.com/questions/21203260/python-get-twitter-trends-in-tweepy-and-parse-json
def trends(woeid):
   """
   WOEIDs:
   Worldwide = 1
   USA = 23424977
   UK = 23424975
   California = 2347563
   Texas = 2347602
   Florida = 2347568
   Los Angeles = 2442047
   """
   trends1 = api.trends_place(woeid)
   trends = dict()
   for trend in trends1[0]['trends']:
      name = trend['name']
      volume = trend['tweet_volume']
      trends[name] = volume
   print(trends)

# https://stackoverflow.com/questions/43982496/cleaning-tweets-nothing-is-displayed
def clean_tweet(tweet):
     '''
     Utility function to clean tweet text by removing links, special characters
     using simple regex statements.
     '''
     tweet = tweet.decode('utf8')
     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-
def get_tweet_sentiment(tweet, tb, writer):
   """ Based on PatternAnalyzer
   analysis = TextBlob(clean_tweet(tweet))
   polarity = analysis.sentiment.polarity
   subjectivity = analysis.sentiment.subjectivity
   print(polarity)
   """

   """
   analysis = TextBlob(clean_tweet(tweet), analyzer=NaiveBayesAnalyzer())
   sentiment = analysis.sentiment
   print(sentiment)
   """

   tweet = clean_tweet(tweet)
   print(tweet)
   analysis = tb(tweet)
   writer.writerow([tweet, str(analysis.sentiment.p_pos), str(analysis.sentiment.p_neg)])
   

#search("The Hitman's Bodyguard", 10, False)
#get_user_info("@BarackObama")
tb = Blobber(analyzer=NaiveBayesAnalyzer())
#tweets = get_user_timeline("@realDonaldTrump", 30)
tweets = search("Kingsman The Golden Circle", 5, False)
with open('textblob.csv', 'w') as csvfile:
   writer = csv.writer(csvfile)
   for i in range(len(tweets)):
      get_tweet_sentiment(tweets[i], tb, writer)
