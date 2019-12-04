import pandas as pd
import glob
import re
import nltk
import matplotlib.pyplot as plt
from textblob import TextBlob



partyKeywords = ['Liberal OR Liberals OR trudeau',
            'conservative OR conservatives OR Scheer',
            'NDP OR _Jagmeet Singh_ OR jagmeetsingh']


# provinces = ['British Columbia', 'New Brunswick', 'Newfoundland and Labrador',
#              'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan']
provinces = ['Aurora--Oak Ridges--Richmond Hill','Barrie--Innisfil','Barrie--Springwater--Oro-Medonte','Bay of Quinte - Baie de Quinte','Beaches--East York','Brampton Centre - Brampton-Centre','Brampton East - Brampton-Est', 'Brampton North - Brampton-Nord','Brampton South - Brampton-Sud', 'Brampton West - Brampton-Ouest','Brantford--Brant','Bruce--Grey--Owen Sound','Burlington','Cambridge','Carleton','Chatham-Kent--Leamington','Davenport','Don Valley East - Don Valley-Est','Don Valley West - Don Valley-Ouest','Dufferin--Caledon','Durham','Eglinton--Lawrence']
# provinces = ['Abbotsford','Acadie--Bathurst','Ahuntsic-Cartierville','Ajax', 'Alfred-Pellan','Argenteuil--La Petite-Nation','Aurora--Oak Ridges--Richmond Hill','Avalon', 'Banff--Airdrie', 'Barrie--Innisfil', 'Barrie--Springwater--Oro-Medonte']
# provinces = ['Guelph','Haldimand--Norfolk','Haliburton--Kawartha Lakes--Brock','Hamilton Centre - Hamilton-Centre',
#              'Hamilton East--Stoney Creek - Hamilton-Est--Stoney Creek','Hamilton Mountain',
#              'Hamilton West--Ancaster--Dundas - Hamilton-Ouest--Ancaster--Dundas'
#             ,'Hastings--Lennox and Addington', 'Humber River--Black Creek', 'Huron--Bruce' , 'Kanata--Carleton' ,
#              'Kingston and the Islands - Kingston et les ├î_les' , 'King--Vaughan' , 'Kitchener Centre - Kitchener-Centre',
#              'Kitchener South--Hespeler - Kitchener-Sud--Hespeler' , 'Kitchener South--Hespeler - Kitchener-Sud--Hespeler' ,
#              'Kitchener--Conestoga' , 'Lambton--Kent--Middlesex', 'Lanark--Frontenac--Kingston',
#              'Leeds--Grenville--Thousand Islands and Rideau Lakes - Leeds--Grenville--Thousand Islands et Rideau Lakes',
#              'London North Centre - London-Centre-Nord', 'London West - London-Ouest', 'London--Fanshawe',
#              'Markham--Stouffville', 'Markham--Thornhill', 'Markham--Unionville', 'Milton',
#              'Mississauga East--Cooksville - Mississauga-Est--Cooksville' , 'Mississauga--Lakeshore'
#     ,  'Mississauga--Malton', 'Nepean', 'Newmarket--Aurora', 'Niagara Centre - Niagara-Centre' , 'Niagara Falls' ,
#              'Niagara West - Niagara-Ouest' , 'Nickel Belt', 'Nipissing--Timiskaming',
#              'Northumberland--Peterborough South - Northumberland--Peterborough-Sud']
final = {}
outcome = {}

for province in provinces:
    for party in partyKeywords:

        data = pd.read_csv("./RD2/politicalTweetsRiding" + party + province + ".csv")

        count = 0
        pos = 0
        neg = 0
        neut = 0

        for line in data.tweet:

            # print(line)
            line = re.sub('[^a-zA-Z0-9_\']', ' ', line)
            line = re.sub(r'^\s', '', line)
            #print(line)
            analysis = TextBlob(line)
            count += 1
            #print(analysis.sentiment.polarity)
            if analysis.sentiment.polarity > 0:
                pos += 1


                # print('positive')
            elif analysis.sentiment.polarity == 0:
                neut += 1
                # print('neutral')
            else:
                neg += 1
                # print('negative')

        print("positive tweets for " + party + province + " is " + str(pos) + " for " + str(count) + " tweets = " + str(
            pos / count))
        print("negative tweets " + party + province + " is " + str(neg) + " for " + str(count) + " tweets = " + str(
            neg / count))
        print("Neutral tweets " + party + province + " is " + str(neut) + " for " + str(count) + " tweets = " + str(
            neut / count))


        max1 = 0
        s = ''
        if pos > neg and pos > neut:
            final[(party , province)] = (pos/count, "pos" , party)
            max1 = pos
            s = ' pos'
        elif neg > neut:
            final[(party , province)] = (neg/count, "neg" , party)
            max1 = neg
            s = ' neg'
        else:
            final[(party, province)] = (neut/count, "neut" , party)
            max1 = neut
            s = ' neut'

print(final)

for province in provinces:
    print(province)
    provinceID = [v for k,v in final.items() if k[1] == province]
    print(provinceID)
    t = max(provinceID, key=lambda item: item[0])
    outcome[province] = t[2]

print(outcome)

