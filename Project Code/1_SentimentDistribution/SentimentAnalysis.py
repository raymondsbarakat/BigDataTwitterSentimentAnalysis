import json

import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
import requests
from textblob import TextBlob
#import geopandas

# import gmplot
#
#
# gmap = gmplot.GoogleMapPlotter.from_geocode("Canada")
# gmap.draw("mymap.html")


# %matplotlib inline
# read the shapefile as a GeoDataFrame


partyKeywords = ['Liberal OR Liberals OR trudeau',
            'conservative OR conservatives OR Scheer',
             'NDP']

provinces = ['British Columbia', 'New Brunswick', 'Newfoundland and Labrador',
             'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan']
# final = {}
# outcome = {}
# for province in provinces:
#     for party in partyKeywords:
#
#         data = pd.read_csv("./data/" + province + "_" + party + ".csv")
#
#         count = 0
#         pos = 0
#         neg = 0
#         neut = 0
#
#         for line in data.tweet:
#             # print(line)
#             line = re.sub('[^a-zA-Z0-9_\']', ' ', line)
#             line = re.sub(r'^\s', '', line)
#             # print(line)
#             analysis = TextBlob(line)
#             count += 1
#             # print(analysis.sentiment.polarity)
#             if analysis.sentiment.polarity > 0:
#                 pos += 1
#
#
#                 # print('positive')
#             elif analysis.sentiment.polarity == 0:
#                 neut += 1
#                 # print('neutral')
#             else:
#                 neg += 1
#                 # print('negative')
#
#         print("positive tweets for " + party + province + " is " + str(pos) + " for " + str(count) + " tweets = " + str(
#             pos / count))
#         print("negative tweets " + party + province + " is " + str(neg) + " for " + str(count) + " tweets = " + str(
#             neg / count))
#         print("Neutral tweets " + party + province + " is " + str(neut) + " for " + str(count) + " tweets = " + str(
#             neut / count))
#
#
#         max1 = 0
#         s = ''
#         if pos > neg and pos > neut:
#             final[(party , province)] = (pos, "pos" , party)
#             max1 = pos
#             s = ' pos'
#         elif neg > neut:
#             final[(party , province)] = (neg, "neg" , party)
#             max1 = neg
#             s = ' neg'
#         else:
#             final[(party, province)] = (neut, "neut" , party)
#             max1 = neut
#             s = ' neut'
#
# print(final)

provinceDict = {}
partyIndicator = 1
for province in provinces:
    provinceDict[province] = partyIndicator
    partyIndicator = (partyIndicator + 1) % 4
print(provinceDict)

# initialize and send the data through REST API
url = 'http://10.24.235.161:5001/updateData'
request_data = json.dumps(provinceDict)
headers = {'content-type': 'application/json'}
print("JSON " + request_data)

response = requests.post(url, data=request_data, headers=headers)

# for province in provinces:
#     print(province)
#     provinceID = [v for k,v in final.items() if k[1] == province]
#     print(provinceID)
#     t = max(provinceID, key=lambda item: item[0])
#     outcome[province] = t[2]
#
# print(outcome)







# can = gpd.GeoDataFrame.from_file("CAN_adm1.shp")
# # The first element
# can.head(5)
# ### many data
# #plot the shapefile/GeoDataFrame
# can.plot()
