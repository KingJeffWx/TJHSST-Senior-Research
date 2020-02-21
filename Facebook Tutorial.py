import sys
import pip
import re
import tweepy
import csv
from textblob import *
from textblob.sentiments import NaiveBayesAnalyzer
import preprocessor as p

"""
References:
https://medium.com/towards-data-science/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999
"""


#Use for installing modules using pip
#pip.main(["install", "tweet-preprocessor"])
