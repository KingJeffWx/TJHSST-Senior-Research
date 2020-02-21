import sys
from importlib import reload
import datetime
import time
import pip
import re
import tweepy
import csv
from textblob import *
from textblob.sentiments import NaiveBayesAnalyzer
import preprocessor as p
from operator import itemgetter

#Use for installing modules using pip
#pip.main(["install", "tweet-preprocessor"])

reload(sys)

data_ratings = []
movie_ids_ratings = []
ratings = []
timestamps = []  # first tweet sent on 02-28-2013

data_movies = []
movie_ids_movies = []
movie_titles = []
genres = []

def parse_ratings(data_ratings, movie_ids_ratings, ratings, timestamps):
    file = open('ratings.dat')
    
    for line in file:
        data_ratings += [line.split()]
    for line in data_ratings:
        string = line[0].split('::')
        movie_ids_ratings.append(string[1])
        ratings.append(string[2])
        timestamps.append(string[3])
    file.close()

def parse_movies(data_movies, movie_ids_movies, movie_titles, genres):
    file = open('movies.dat', encoding='utf8')

    for line in file:
        data_movies += [line]
    for line in data_movies:
        string = line.split('::')
        should_add = True
        for year in range(1800, 2013):  # Do not include movies before 2011
            if str(year) in string[1]:
                should_add = False
        if should_add:
            movie_ids_movies.append(string[0])
            movie_titles.append(string[1])
            genres.append(string[2].strip('\n'))
    file.close()

def count_ratings(movie_id, movie_ids_ratings): # count how many ratings a movie has received
    count = 0
    for r in movie_ids_ratings:
        if movie_id == r:
            count += 1
    return count

def avg_rating(movie_id, movie_ids_ratings, ratings, count_ratings):   # compute the average rating of a movie
    total_rating = 0
    for i in range(len(ratings)):
        if movie_id == movie_ids_ratings[i]:
            total_rating += int(ratings[i])
    avg_rating = total_rating / count_ratings
    return avg_rating

def movie_to_id(title, movie_ids_movies, movie_titles): # get a movie id given its title
    for i in range(len(movie_titles)):
        if title == movie_titles[i]:
            return movie_ids_movies[i]
    return None

def id_to_movie(movie_id, movie_ids_movies, movie_titles): # get movie title from id
    for i in range(len(movie_titles)):
        if movie_id == movie_ids_movies[i]:
            return movie_titles[i]
    return None

def most_ratings(movie_ids_ratings, movie_ids_movies, movie_titles, number):    # which movies have the most ratings
    most_ratings = []
    for i in range(len(movie_titles)):
        count = count_ratings(movie_ids_movies[i], movie_ids_ratings)
        pair = (count, movie_titles[i])
        most_ratings.append(pair)
    most_ratings.sort(key=itemgetter(0))
    most_ratings.reverse()
    for i in range(number):
        print(most_ratings[i])

def get_timestamps(timestamps):
    for t in timestamps: # print out times in readable format
        print(datetime.datetime.utcfromtimestamp(int(t)).strftime('%Y-%m-%dT%H:%M:%SZ'))

def write_data():
    start = time.time()
    file = open("MovieTweetings.txt", "w", encoding="utf8")
    for i in range(len(movie_titles)):
        movie_id = movie_to_id(movie_titles[i], movie_ids_movies, movie_titles)
        r_count = count_ratings(movie_id, movie_ids_ratings)
        if r_count >= 100:
            a_rating = avg_rating(movie_id, movie_ids_ratings, ratings, r_count)
            file.write(movie_titles[i] + '\t' + str(r_count) + '\t' + str(a_rating) + '\n')
    file.close()
    done = time.time()
    elapsed = done - start
    print(elapsed)

parse_ratings(data_ratings, movie_ids_ratings, ratings, timestamps)
parse_movies(data_movies, movie_ids_movies, movie_titles, genres)

"""
count_ratings('0451279', movie_ids_ratings)
avg_rating('0451279', movie_ids_ratings, ratings)
movie_to_id('Wonder Woman (2017)', movie_ids_movies, movie_titles)
id_to_movie('0451279', movie_ids_movies, movie_titles)
"""
#most_ratings(movie_ids_ratings, movie_ids_movies, movie_titles, 100)
write_data()
