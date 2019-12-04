import pandas as pd
from scipy.spatial import distance
import twint
# import numpy as np
# from sklearn.metrics.pairwise import euclidean_distances

centers = {}
dist = {}
c = twint.Config()
geoL = {}

def centeroidnp(x, y):
    length = len(y)
    #print(x, length)
    sum1 = map(sum, zip(*y))
    listSum = list(sum1)
    centers[x] = (listSum[0]/length, listSum[1]/length)


def radiusAprox(x, y):
        cent = centers[x]
        coor = [tuple(l) for l in y]
        #print(str(cent) + " coor: " + str(coor))
        rad = distance.pdist(y, 'euclidean')
        mm = sum(rad)/len(coor)
        #print(x, mm)
        # d = euclidean_distances(cent, k)
        dist[x] = mm


data = pd.read_csv("./data/FederalRidings.csv",  encoding='latin-1')

df = data[[' FEDname/CEFnom',' DArplat/Adlat', ' DArplong/ADlong']]

pf = df.groupby(' FEDname/CEFnom')[' DArplat/Adlat',' DArplong/ADlong'].apply(lambda x: x.values.tolist()).to_dict()

# for x in pf:
#     print(x)

for x, y in pf.items():
    #print(x,y)
    centeroidnp(x, y)

for x, y in pf.items():
    radiusAprox(x, y)

for x, y in centers.items():
    geoL[x]= (y , dist[x])

for x, y in geoL.items():
    print(x, y)

partyKeywords =['Liberal OR Liberals OR trudeau',
                   'conservative OR conservatives OR Scheer']
                   #'\"NDP OR Jagmeet Singh\"']


for party in partyKeywords:
    for x ,y in geoL.items():
        c.Search = party
        c.Since = "2015-10-21 00:00:00"
        c.Until = "2019-10-21 00:00:00"
        if 100*y[1] > 150:
            break
        c.Geo = str(y[0][0]) + "," + str(y[0][1]) + "," + str(100*y[1]) + "km"
        #c.Geo = "43.65881690934842, -79.36997665439088, 2.0501943141372016km"
        tweets = []
        c.Store_object = True
        c.Store_object_tweets_list = tweets

        # c.Since = str(datetime.datetime.strptime("2019-07-21 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()).split('.')[0]
        # c.Until = str(datetime.datetime.strptime("2019-07-21 00:00:00", "%Y-%m-%d %H:%M:%S").timestamp()).split('.')[0]
        c.Store_csv = True
        c.Output = "./RidingData/politicalTweetsRiding" + party + x +".csv"
        twint.run.Search(c)