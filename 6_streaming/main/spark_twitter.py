from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SQLContext
import pyspark
import sys
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()

# list of hashtags
searched_hashtags = [
         # CANADA
         '#canada', '#canadian', '#canadians', '#poutine', '#canadaimmigration', '#canadiangovernment', '#liberals', '#clp', '#toronto', '#eh',
         # USA
         '#USA', '#america', '#american', '#americans', '#americanimmigration', '#americangovernment', '#trump', '#conservatives', '#NYC', '#newyork',
         # GREECE
         '#greece', '#greek', '#greeks', '#athens', '#sirtaki', '#greekgovernment', '#greecelife', '#moussaka', '#santorini', '#pavlopoulos',
         # FRANCE
         '#france', '#french', '#francais', '#crepe', '#crepes', '#wine', '#eiffeltower', '#paris', '#toureiffel', '#macron',
         # INDIA
         '#india', '#indian', '#hindi', '#namaste', '#mumbai', '#bollywood', '#chai', '#butterchicken', '#samosa', '#newdelhi']

# create spark configuration
conf = SparkConf()
conf.setAppName("Countries Twitter Sentiment Analysis")

# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

# create the Streaming Context from spark context, interval size 2 seconds
ssc = StreamingContext(sc, 2)

# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")

# read data from port 9009
dataStream = ssc.socketTextStream("twitter", 9009)

# decide whether tweet will be chosen or not
def chooseTweet(tweet):
    for hashtag in searched_hashtags:
        if hashtag in tweet:
            return True

    return False


def getTopic(goodTweet):
    for hashtag in searched_hashtags:
        if hashtag in goodTweet:
            tagIndex = searched_hashtags.index(hashtag)

            if tagIndex < 10:
                return "Canada"
            elif tagIndex < 20:
                return "USA"
            elif tagIndex < 30:
                return "Greece"
            elif tagIndex < 40:
                return "France"
            else:
                return "India"


def sentimentAnalysis(goodTweet):
    scores = sia.polarity_scores(goodTweet)
    compound_score = scores['compound']

    if compound_score > 0.2:
        return (1, 1)
    elif compound_score < - 0.1:
        return (-1, 1)
    else:
        return (0, 1)


# get good tweets that have our hashtags
goodTweet = dataStream.filter(lambda tweet: chooseTweet(tweet.lower().split()))

# map as follows: topic --> (s, c)
sentimentCount = goodTweet.map(lambda tweet: (getTopic(tweet.lower().split()), sentimentAnalysis(tweet.lower())))


# adding the (sentiment, count) of each topic to its last (sentiment, count)
def aggregate_tags_count(new_values, prev_values):
    sentimentValue = sum(valueTuple[0] for valueTuple in new_values) + (prev_values[0] if prev_values else 0)
    totalCount     = sum(valueTuple[1] for valueTuple in new_values) + (prev_values[1] if prev_values else 0)

    return (sentimentValue, totalCount)


# do the aggregation, note that now this is a sequence of RDDs
sentiment_totals = sentimentCount.updateStateByKey(aggregate_tags_count)


def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']


def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        # if rdd is empty, then exit. The main reason behind exiting is
        # to avoid getting ValueError Exception, which will be printed since we are
        # catching all exception and printing them
        if rdd.isEmpty():
            return

        # Get spark sql singleton context from the current context
        sql_context = get_sql_context_instance(rdd.context)

        # convert the RDD to Row RDD
        row_rdd = rdd.map(lambda w: Row(topic=w[0], sentiment=w[1][0] / w[1][1]))

        # create a DF from the Row RDD
        sentiment_df = sql_context.createDataFrame(row_rdd)

        # Register the dataframe as table
        sentiment_df.registerTempTable("topics")

        # get the country sentiments from the table using SQL and print them
        sentiment_counts_df = sql_context.sql("select topic, sentiment from topics order by sentiment desc")
        sentiment_counts_df.show()

        # call this method to prepare top 10 hashtags DF and send them
        send_df_to_dashboard(sentiment_counts_df)
    except:
        e = sys.exc_info()[0]
    # print("Error: %s" % e)


def send_df_to_dashboard(df):
    # extract the hashtags from dataframe and convert them into array
    top_tags = [str(t.topic) for t in df.select("topic").collect()]
    # extract the counts from dataframe and convert them into array
    tags_count = [p.sentiment for p in df.select("sentiment").collect()]
    # initialize and send the data through REST API
    url = 'http://192.168.0.11:5001/updateData'
    request_data = {'label': str(top_tags), 'data': str(tags_count)}
    response = requests.post(url, data=request_data)


# do this for every single interval
sentiment_totals.foreachRDD(process_rdd)

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()


