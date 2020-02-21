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
#pip.main(["install", "beautifulsoup4"])

reload(sys)

movie_ids = dict()  # each key has: movie title, genres, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 star ratings, total rating score
movie_links = []
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
            for year in range(1800, 2010):  # Do not include movies before 2011
                if str(year) in string[1]:
                    should_add = False
            if should_add:
                movie_id = string[0]
                movie_title = string[1]
                genres = string[2].strip('\n')
                movie_ids[movie_id] = [movie_title, genres, 0,0,0,0,0,0,0,0,0,0, 0.0]
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
        file.write(str(movie[12]) + '\n')
    file.close()
    done = time.time()
    elapsed = done - start
    print(elapsed)

def scrape_movielinks():
    start = time.time()
    current_url = "http://www.boxofficemojo.com/movies/alphabetical.htm?letter=NUM&p=.htm"  # starting point for search

    soup = BeautifulSoup(urllib.request.urlopen(current_url).read(), "html5lib")
    letters = soup.findAll('a', href= re.compile('letter='))
    letter_index = []
    for t in letters:
        letter_index.append("http://www.boxofficemojo.com" + t['href'])

    for i in range(1): # loop through all letter 27 indices for movies
        current_url = letter_index[i]
        soup = BeautifulSoup(urllib.request.urlopen(current_url).read(), "html5lib")
        navbar = soup.find('div', 'alpha-nav-holder')
        pages = navbar.findAll('a', href= re.compile('alphabetical'))
        page_list = []
        for t in pages:
            page_list.append("http://www.boxofficemojo.com" + t['href'])
        movietable = soup.find('div', {'id':'main'})
        movies = movietable.findAll('a', href= re.compile('id='))
        for t in movies:
            movie_links.append("http://www.boxofficemojo.com" + t['href'])
        if pages != None:   # this only runs if there's a 2nd page for this letter
            i = 0
            while i < len(page_list):
                current_url = page_list[i]
                soup = BeautifulSoup(urllib.request.urlopen(current_url).read(), "html5lib")
                movietable = soup.find('div', {'id':'main'})
                movies = movietable.findAll('a', href= re.compile('id='))
                for t in movies:
                    movie_links.append("http://www.boxofficemojo.com" + t['href'])
                i += 1
        if i % 9 == 0:
            print(len(movie_links)) # prevent it from crashing
    done = time.time()
    elapsed = done - start
    print(elapsed)

def scrape_boxoffice(movie_links):
    start = time.time()
    for url in movie_links:
        if "elizabeth" in url and "elizabethtown" not in url:
            url = 'http://www.boxofficemojo.com/movies/?id=elizabeth%A0.htm'
        if "simpleplan" in url:
            url = 'http://www.boxofficemojo.com/movies/?id=simpleplan%A0.htm'
        current_url = url
        soup = BeautifulSoup(urllib.request.urlopen(current_url).read(), "html5lib")

        all_bs = soup.findAll('b')
        b_list = []
        for t in all_bs:
            item = t.encode_contents().decode('utf-8')
            if 'Domestic Lifetime' not in item:
                b_list.append(item)
        if len(b_list) >= 10:   # avoids bad entries with no box office data
            if '$' in b_list[2] or 'n/a' in b_list[9]:
                if 'n/a' in b_list[9]:  # has foreign release only, order is shifted
                    title = b_list[1]
                    domestic = 'N/A'
                    genre = b_list[4]
                    runtime = b_list[5]
                    rating = b_list[6]
                    budget = b_list[7]
                    worldwide = b_list[12]
                else:   # domestic release
                    title = b_list[1]
                    domestic = b_list[2]
                    genre = b_list[5]
                    runtime = b_list[6]
                    rating = b_list[7]
                    budget = b_list[8]
                    if len(b_list) == 11 or '%' not in b_list[11]:
                        worldwide = 'N/A'
                    else:
                        worldwide = b_list[13]
    done = time.time()
    elapsed = done - start
    print(elapsed)
                    

scrape_movielinks()
scrape_boxoffice(movie_links)
parse_movies(movie_ids)
print(movie_ids['100083'])
parse_ratings(movie_ids)
print(movie_ids['100083'])
write_data()

"""
count_ratings('0451279', movie_ids_ratings)
avg_rating('0451279', movie_ids_ratings, ratings)
movie_to_id('Wonder Woman (2017)', movie_ids_movies, movie_titles)
id_to_movie('0451279', movie_ids_movies, movie_titles)
"""
