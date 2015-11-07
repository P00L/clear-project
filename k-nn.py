import csv
import datetime
from similarity import cosine_sim, top_n_match, similarity_pearson
__author__ = 'Alessandro'


def get_knn_recommendations(urm, user, knn):
    """
    RIGHT NOW IT'S KINDA CRAP, WE DON'T DO ANYTHING BUT BUILDING FILES HERE
    """
    totals = {}
    sim_sums = {}
    for neighbor in knn[user]:
        for movie in urm[neighbor]:
            if movie not in urm[user]:
                totals.setdefault(movie, 0)
                # totals = {movie: sum of rating weighted by similarity
                totals[movie] += urm[neighbor][movie] * knn[user][neighbor]
                sim_sums.setdefault(movie, 0)
                sim_sums[movie] += knn[user][neighbor]
    rankings = [(total / sim_sums[movie], movie) for total, movie in totals.items()]
    return sorted(rankings, key=lambda x: -x[0])[0:5]


def get_top_n_recommendations(urm, user, knn):
    """
    RIGHT NOW IT'S KINDA CRAP, WE DON'T DO ANYTHING BUT BUILDING FILES HERE
    """
    avg_rec = [(5.0, 33173), (5.0, 33475), (5.0, 1076), (5.0, 35300), (5.0, 15743)]
    seen_movies = {}
    rankings = {}
    sim_sums = {}
    rec = []
    # build a dictionary of film seen by neighbours
    for neighbor in knn[user]:
        for movie in urm[neighbor]:
            if movie not in urm[user]:
                seen_movies.setdefault(movie, {}).setdefault(neighbor)
                seen_movies[movie][neighbor] = urm[neighbor][movie]
    for movie in seen_movies:
        rankings.setdefault(movie, 0)
        for neighbor in seen_movies[movie]:
            rankings[movie] += seen_movies[movie][neighbor]*knn[user][neighbor]
            sim_sums[movie] += knn[user][neighbor]
        rankings[movie] /= sim_sums[movie]
        rec = sorted(rankings, key=lambda x: -x[0])[0:5]

    return rec


urm = {}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    # create a nested dict; {userId: {movieId: rating}}
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]), {}).setdefault(int(row[1]))
            urm[int(row[0])][int(row[1])] = float(row[2])
print('computing right now')
time = datetime.datetime.now()
print(top_n_match(urm, 4, 7, similarity=similarity_pearson))
print(datetime.datetime.now() - time)

test = {}
time = datetime.datetime.now()
with open('resources/test.csv') as test_raw:
    reader = csv.reader(test_raw)
    # create a nested dict for test user
    for row in reader:
        if row[0] != 'userId':
            test[int(row[0])] = top_n_match(urm, int(row[0]), 10, similarity=cosine_sim)
            print('fatto user: ' + row[0])
print(datetime.datetime.now() - time)
print(len(test))

"""
IMPORTANT --> if you can, submit the file in this format
* k-nn-_[similarity]_[shrink].csv
(substitute similarity with 'cosine' or 'pearson' and shrink with the actual value)
THANKS
"""
with open('resources/k-nn_cosine_user_10.csv', 'w') as knn_raw:
    fieldnames = ['userId', 'neighborId', 'similarity']
    w = csv.DictWriter(knn_raw, fieldnames=fieldnames)
    w.writeheader()
    for user in sorted(test):
        for other in test[user]:
            knn_raw.write(str(user) + ',' + str(other) + ',' + str(test[user][other]) + '\n')
