import re
import socket
import sys
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream

# Tweepy API Credentials
CONSUMER_KEY = "vNQdccsU7qD8qCA5LRjZKxvNN"
CONSUMER_SECRET = "7rmevS3tbpdjMlmvXsSh0IYHW9iVF01vkIx5zi3ytGs0gBWUjg"
ACCESS_TOKEN = "942120259569496066-jUr59FJ1pz1tBOOc9PsOD33X5P9aTrV"
ACCESS_TOKEN_SECRET = "trv7xnaAs5ieWW0X0UlcbjsVQjwXXMu3dgqot8FbJ6dpB"


# Listener for tweet streams
class TweetListener(StreamListener):
    def on_data(self, data):
        try:
            global conn
            full_tweet = json.loads(data)

            # Get tweet text from JSON
            tweet_text = full_tweet['text']

            # print tweet
            print("------------------------------------------")

            # Tweet cleaning
            tweet_text = cleanTweet(tweet_text)
            print(tweet_text + '\n')

            # send tweet to Spark
            conn.send(str.encode(tweet_text + '\n'))
        except:
            # handle errors
            e = sys.exc_info()[0]
            print("Error: %s" % e)

        return True

    def on_error(self, status):
        print(status)


# remove special symbols and numbers..etc.
def cleanTweet(tweet):
    tweet = re.sub(r'[^[a-zA-Z#\s]+|[^[a-zA-Z#\s]+$', '', tweet)
    tweet = re.sub(r'[\s]+', ' ', tweet)
    return tweet


# IP and port of local machine or Docker
TCP_IP = socket.gethostbyname(socket.gethostname())  # returns local IP
TCP_PORT = 9009

# setup local connection, expose socket, listen for spark app
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")

# if the connection is accepted, proceed
conn, addr = s.accept()
print("Connected... Starting getting tweets.")

# ==== setup twitter connection ====
listener = TweetListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream = Stream(auth, listener)

# setup search terms
track = [ # CANADA
         '#canada', '#canadian', '#canadians', '#poutine', '#canadaimmigration', '#canadiangovernment', '#liberals', '#clp', '#toronto', '#eh',
         # USA
         '#USA', '#america', '#american', '#americans', '#americanimmigration', '#americangovernment', '#trump', '#conservatives', '#NYC', '#newyork',
         # GREECE
         '#greece', '#greek', '#greeks', '#athens', '#sirtaki', '#greekgovernment', '#greecelife', '#moussaka', '#santorini', '#pavlopoulos',
         # FRANCE
         '#france', '#french', '#francais', '#crepe', '#crepes', '#wine', '#eiffeltower', '#paris', '#toureiffel', '#macron',
         # INDIA
         '#india', '#indian', '#hindi', '#namaste', '#mumbai', '#bollywood', '#chai', '#butterchicken', '#samosa', '#newdelhi']
language = ['en']

# get filtered tweets, forward them to spark until interrupted
try:
    stream.filter(track=track, languages=language)
except KeyboardInterrupt:
    s.shutdown(socket.SHUT_RD)

