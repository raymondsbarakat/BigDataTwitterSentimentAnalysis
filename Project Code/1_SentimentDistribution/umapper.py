import sys
import re
import csv
import nltk

# Below code splits the user comment into words and calculates the ngrams. Then prints each ngram along with 1.
# Key: ngram Value: 1

for row in csv.reader(iter(sys.stdin.readline, '')):
    words = re.split(r'\W+', row[9])
    grams = nltk.ngrams(words, 1)
    for gram in grams:
        if ''.join(gram):
            print(' '.join(gram).lower() + ' 1')