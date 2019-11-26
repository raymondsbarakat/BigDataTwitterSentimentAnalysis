import csv
import re

from pandas._libs import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from textblob import TextBlob

#Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = "942120259569496066-jUr59FJ1pz1tBOOc9PsOD33X5P9aTrV"
ACCESS_TOKEN_SECRET = "trv7xnaAs5ieWW0X0UlcbjsVQjwXXMu3dgqot8FbJ6dpB"
CONSUMER_KEY = "vNQdccsU7qD8qCA5LRjZKxvNN"
CONSUMER_SECRET = "7rmevS3tbpdjMlmvXsSh0IYHW9iVF01vkIx5zi3ytGs0gBWUjg"


#HappyEmoticons
emoticons_happy = [
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ]

# Sad Emoticons
emoticons_sad = [
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ]

ON = ["ontario", "on"]
QC = ["quebec", 'qc']
AB = ["alberta", "ab"]
MB = ["manitoba", "mb"]
NS = ["nova",  "scotia", "ns"]
BC = ["british",  "columbia", "bc"]
NB = ["brunswick", "nb"]
NL = ["newfoundland",  "labrador", "nl"]
PE = ["prince",  "edward", "island", "pe"]
SASK = ["saskatchewan", "sask"]

provinces = ["ontario", "on", "quebec", 'qc',"alberta", "ab", "manitoba", "mb", "nova scotia", "ns",
             "british columbia", "bc","new brunswick", "nb", "newfoundland and labrador", "nl",
             "prince edward island", "pe", "saskatchewan", "sask"]

sia = SIA()


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):


    def on_data(self, data):
        # global conn
        full_tweet = json.loads(data)

        # Get tweet text from JSON
        tweet_text = full_tweet['text']
        # tweet_location = full_tweet['user']['location']
        tweet_location = filterLocation(full_tweet)
        # tweet_place = full_tweet['place']
        # tweet_coordinates = full_tweet['coordinates']


        # print tweet
        print("------------------------------------------")

        # Tweet cleaning
        # tweet_text = cleanTweet(tweet_text)
        if tweet_location:
            print(tweet_text + " [" + tweet_location + "]" '\n')


        # parseAndLabelTweet(clean_tweet(tweet_text))

        # send tweet to Spark
        # conn.send(str.encode(tweet_text + '\n'))

        # handle errors
        # e = sys.exc_info()[0]
        # print("Error: %s" % e)
        return True

    def on_error(self, status):
        print (status)


def isProvince(locationTokens, provinceList):
    for element in provinceList:
        for token in locationTokens:
            if token.strip() == element.strip():
                print("comparing: " + token + " vs. " + element)
                return True

    return False


def getProvince(location):
    print("chosen location: " + location)
    location = location.split()
    print(location)



    if isProvince(location, ON):
        return "Ontario"
    elif isProvince(location, QC):
        return "Quebec"
    elif isProvince(location, AB):
        return "Alberta"
    elif isProvince(location, MB):
        return "Manitoba"
    elif isProvince(location, NS):
        return "Nova Scotia"
    elif isProvince(location, BC):
        return "British Columbia"
    elif isProvince(location, NB):
        return "New Brunswick"
    elif isProvince(location, NL):
        return "Newfoundland and Labrador"
    elif isProvince(location, PE):
        return "Prince Edward Island"
    elif isProvince(location, SASK):
        return "Saskatchewan"
    else:
        return None

def filterProvince(location):
    for province in provinces:
        if province in location:
            return getProvince(location)

    return None


def filterLocation(tweet):
    tweet_location = tweet['user']['location']
    if tweet_location:
        tweet_location = re.sub(r'[^[a-zA-Z\s]+|[^[a-zA-Z\s]+$', '', tweet_location)
        tweet_location = re.sub(r'[\s]+', ' ', tweet_location)
        tweet_location = tweet_location.lower()
        # print(tweet_location)
        tweet_location = filterProvince(tweet_location)


    return tweet_location



def labelPositive(tweet):
    row = [tweet, 'POSITIVE']
    with open('labelPositive.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()

def labelNegative(tweet):
    row = [tweet, 'NEGATIVE']
    with open('labelNegative.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()

def labelNeutral(tweet):
    # scores = sia.polarity_scores(tweet)
    # m = max(scores['pos'], scores['neg'], scores['neu'])
    # if (m == scores['neu']):
    print(">>>>>>neutral tweet!<<<<<<<<")

    row = [tweet, 'NEUTRAL']
    with open('labelNeutral.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()

def parseAndLabelTweet(tweet):
    score = TextBlob(tweet)
    sentiment = score.sentiment.polarity
    if sentiment > 0:
        labelPositive(tweet)
    elif sentiment == 0:
        labelNeutral(tweet)
    else:
        labelNegative(tweet)
    # for happy in emoticons_happy:
    #     if happy in tweet:
    #         labelPositive(tweet)
    #         print(">>>>>>positive tweet!<<<<<<<<")
    #         return
    #
    # for sad in emoticons_sad:
    #     if sad in tweet:
    #         labelNegative(tweet)
    #         print(">>>>>>negative tweet!<<<<<<<<")
    #
    #         return
    #
    # labelNeutral(tweet)
    # return

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)", " ", tweet).split())

if __name__ == '__main__':
    track = [
        # LIBERALS
        '#liberal', '#liberals', '#lpc', '#trudeau', '#justintrudeau', 'justintrudeau', 'trudeau', 'liberal',
        'liberals', 'Liberal Party of Canada', 'Justin Trudeau'
        # CONSERVATIVES
                                               '#conservatives', '#conservative', '#cpc', '#scheer', '#andrewscheer',
        'conservatives', 'conservative', 'cpc',
        'Andrew Scheer', 'Scheer', 'Conservative Party of Canada',
        # NDP
        '#NDP', '#newdemocraticparty', '#jagmeetsingh', '#jagmeet', 'NDP', 'new democratic party', 'jagmeet singh',
        'jagmeet']
    language = ['en']
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)

    stream.filter(track=track, languages=language)
