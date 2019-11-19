#! /Library/Frameworks/Python.framework/Versions/3.7/bin/pip3

import twint
c = twint.Config()







# c = twint.Config()
c.Search = "Liberal OR Liberals OR conservative OR conservatives OR NDP OR \"New democratic party\" OR trudeau OR scheer OR \"Jagmeet Singh\""
# c.Search = "Liberal OR conservative OR Jagmeet Singh"

# c.Search = "liberal"

# c.Min_likes = 5
# c.Store_json = True
# c.Location=True
c.Near="Ontario"
# c.Geo = "43.634380,-79.789842,1000000km"
tweets = []
c.Store_object = True
c.Store_object_tweets_list = tweets
c.Since="2019-7-21"
c.Until="2019-10-21"
c.Store_csv = True
c.Output = "file6.csv"
twint.run.Search(c)

# for tweet in tweets:
#     print("================")
#     print(str(tweet['created_at']))