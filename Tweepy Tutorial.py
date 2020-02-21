import tweepy

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
   for i in range(len(text_list)):
      print(text_list[i], retweets_list[i], likes_list[i])

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
   for i in range(len(text_list)):
      print(text_list[i], date_list[i])
      

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

def clean_tweet(tweet):
     '''
     Utility function to clean tweet text by removing links, special characters
     using simple regex statements.
     '''
     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#search("The Hitman's Bodyguard", 10, False)
#get_user_timeline("@BarackObama", 10)
get_user_info("@BarackObama")
