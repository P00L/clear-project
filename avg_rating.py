__author__ = 'Federica'
import csv
import collections
f = open('resources/train.csv', 'r')
file = csv.reader(f)
movie_ratings = {}

# create dictionary from csv file containin {'itemId': 'rating':}
for row in file:
    if row[0] != "userId":
        movie_ratings.setdefault(row[1], []).append(float(row[2]))

# compute the average for all ratings for movies, with shrink factor
for keys in movie_ratings:
    sum = 0
    for item in movie_ratings[keys]:
        sum += item
    movie_ratings[keys] = sum / (len(movie_ratings[keys]) + 8)

# dictionary becomes a list ordered by ratings
top_movies = sorted(movie_ratings.items(), key = lambda x: -x[1])
print(top_movies)

# open test to retrieve all users id necessary saved in a list
f = open('resources/test.csv', 'r')
test = csv.reader(f)
user = list(test)
user.pop(0)
print(user)

# list of the five top-rated movies
movie = ''
for i in range(5):
    movie = movie + str(top_movies[i][0]) + ' '
print("movie:" + str(movie))

# create dictionary for the writing

final_dic = {}
for i in range(0,len(user)):
    final_dic[int(user[i][0])] = movie

# now we write the cvs file
from operator import  itemgetter
with open('submission/avg.csv', 'w', newline='') as f:
    dict = {}
    fieldnames = ['userId','testItems']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for i in range(0,len(user)):
        dict['userId'] = user[i][0]
        dict['testItems'] = movie
        w.writerow(dict)
    print(dict)







