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
import urllib
from bs4 import BeautifulSoup

#Use for installing modules using pip
#pip.main(["install", "scikit-learn"])

reload(sys)

movie_ids = dict()  # each key has: movie title, genres, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 star ratings, total rating score, budget, worldwide gross
movie_links = []
movie_budgets = dict()
"""
data_ratings = dict()
movie_ids_ratings = []
ratings = []
timestamps = []

data_movies = dict()
movie_ids_movies = []
movie_titles = []
genres = []
"""

def parse_ratings(movie_ids):
    file = open('ratings.csv')
    line_num = 0
    start = time.time()
    for line in file:
        if line_num > 0:
            line = line.strip()
            string = line.split(',')
            if int(string[3]) > 0:
                movie_id = string[1]
                if movie_id in movie_ids:
                    if float(string[2]) == 0.5:
                        movie_ids[movie_id][2] += 1
                    if float(string[2]) == 1.0:
                        movie_ids[movie_id][3] += 1
                    if float(string[2]) == 1.5:
                        movie_ids[movie_id][4] += 1
                    if float(string[2]) == 2.0:
                        movie_ids[movie_id][5] += 1
                    if float(string[2]) == 2.5:
                        movie_ids[movie_id][6] += 1
                    if float(string[2]) == 3.0:
                        movie_ids[movie_id][7] += 1
                    if float(string[2]) == 3.5:
                        movie_ids[movie_id][8] += 1
                    if float(string[2]) == 4.0:
                        movie_ids[movie_id][9] += 1
                    if float(string[2]) == 4.5:
                        movie_ids[movie_id][10] += 1
                    if float(string[2]) == 5.0:
                        movie_ids[movie_id][11] += 1
                    movie_ids[movie_id][12] += float(string[2])    # add rating score
        line_num += 1
    file.close()
    done = time.time()
    elapsed = done - start
    print(elapsed)

def parse_movies(movie_ids):
    file = open('movies.csv', encoding='utf8')
    line_num = 0
    start = time.time()
    for line in file:
        if line_num > 0:
            line = line.strip()
            if '"' in line:
                string = line.split('"')
                string[0] = string[0].replace(',', '')
                string[2] = string[2].replace(',', '')
            else:
                string = line.split(',')
            should_add = True
            for year in range(1800, 2000):  # Do not include movies before 2011
                if str(year) in string[1]:
                    should_add = False
            if should_add:
                movie_id = string[0]
                movie_title = string[1]
                genres = string[2].strip('\n')
                movie_ids[movie_id] = [movie_title, genres, 0,0,0,0,0,0,0,0,0,0, 0.0, None, None, None]
        line_num += 1
    file.close()
    done = time.time()
    elapsed = done - start
    print(elapsed, len(movie_ids))
"""
def count_ratings(movie_id, movie_ids_ratings): # count how many ratings a movie has received
    count = 0
    start = time.time()
    for r in movie_ids_ratings:
        if movie_id == r:
            count += 1
    done = time.time()
    elapsed = done - start
    print(elapsed, count)
    return count

def avg_rating(movie_id, movie_ids_ratings, ratings, count_ratings):   # compute the average rating of a movie
    total_rating = 0
    for i in range(len(ratings)):
        if movie_id == movie_ids_ratings[i]:
            total_rating += float(ratings[i])
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
"""
def write_data():
    start = time.time()
    file = open("MovieLens Movie Ratings.txt", "w", encoding="utf8")
    for movie in movie_ids.values():
        file.write(movie[0] + '\t')
        file.write(movie[1] + '\t')
        file.write(str(movie[2]) + '\t')
        file.write(str(movie[3]) + '\t')
        file.write(str(movie[4]) + '\t')
        file.write(str(movie[5]) + '\t')
        file.write(str(movie[6]) + '\t')
        file.write(str(movie[7]) + '\t')
        file.write(str(movie[8]) + '\t')
        file.write(str(movie[9]) + '\t')
        file.write(str(movie[10]) + '\t')
        file.write(str(movie[11]) + '\t')
        file.write(str(movie[12]) + '\t')
        file.write(str(movie[13]) + '\t')
        file.write(str(movie[14]) + '\t')
        file.write(str(movie[15]) + '\n')
    file.close()
    done = time.time()
    elapsed = done - start
    print(elapsed)

def scrape_budgets():
    start = time.time()
    url_id = 1
    table_rows = []
    while url_id <= 5401:
        current_url = "http://www.the-numbers.com/movie/budgets/all/" + str(url_id)
        soup = BeautifulSoup(urllib.request.urlopen(current_url).read(), "html5lib")
        for node in soup.findAll('td'):
            table_rows.append(''.join(node.findAll(text=True)))
        url_id += 100
    i = 0
    while i < len(table_rows):
        movie_budgets[i] = [table_rows[i+1], table_rows[i+2], table_rows[i+3], table_rows[i+4], table_rows[i+5]]
        # for each: release date, movie title, budget, domestic, worldwide
        i += 6
    done = time.time()
    elapsed = done - start
    print(elapsed)
    
def budgets_to_movies():    # match budgets to movies
    start = time.time()
    count = 0
    for movie_info in movie_budgets.values():
        release_date = movie_info[0].split('/')
        year = release_date[2]
        month = release_date[0]
        movie_title = movie_info[1]
        budget = movie_info[2]
        domestic = movie_info[3]
        worldwide = movie_info[4]
        movie_title_words = re.sub("[^\w]", " ",  movie_title).split()
        possible_matches = list()
        for movie_ids_info in movie_ids.values():
            movie_ids_title = movie_ids_info[0]
            movie_ids_title_words = re.sub("[^\w]", " ",  movie_ids_title).split()
            shouldAdd = True
            for word in movie_title_words:
                if word not in movie_ids_title_words:
                    shouldAdd = False
            if shouldAdd:
                possible_matches.append(movie_ids_title)
        new_possible_matches = list()
        for i in range(len(possible_matches)):
            year_of_release = possible_matches[i].split('(')[-1].split(')')[0]
            if year == year_of_release:
                new_possible_matches.append(possible_matches[i])
        if len(new_possible_matches) == 1:
            for movie_ids_info in movie_ids.values():
                if movie_ids_info[0] == new_possible_matches[0]:
                    movie_ids_info[13] = budget
                    movie_ids_info[14] = worldwide
                    movie_ids_info[15] = month
        count += 1
    done = time.time()
    elapsed = done - start
    print(elapsed)
                
        

scrape_budgets()
parse_movies(movie_ids)
budgets_to_movies()
#print(movie_ids['100083'])
parse_ratings(movie_ids)
#print(movie_ids['100083'])
write_data()

"""
count_ratings('0451279', movie_ids_ratings)
avg_rating('0451279', movie_ids_ratings, ratings)
movie_to_id('Wonder Woman (2017)', movie_ids_movies, movie_titles)
id_to_movie('0451279', movie_ids_movies, movie_titles)
"""
