from similarity import top_n_match, cosine_sim
import csv
from datetime import datetime


def get_top_n_recommendations(urm, user, knn, n=5, shrink=10):
    """
    * TODO:
        # have a look if a change in shrink on cosine and/or on recommendations gives better score

    This function returns the recommendations based on the k-nn data set already precomputed

    * SCORING:
        216 with 10 of shrink on k-NN_cosine data set (it was computed with 7 of shrink term)

    INPUT PARAMETERS:
    :param urm: the user rating matrix
    :param user: ID of the user i want recommendations
    :param knn: the k-nn dictionary
    :param n: number of recommendations i want (DEFAULT is 5)
    :param shrink: the shrink term to be applied (DEFAULT is 10)

    OUTPUT
    :return: a list of tuples (value, movieId) containing the recommendations

    """
    avg_rec = [(5.0, 33173), (5.0, 33475), (5.0, 1076), (5.0, 35300), (5.0, 15743)]
    seen_movies = {}
    rankings = {}
    sim_sums = {}
    recommendations = []

    if user in knn:
        # build a dictionary of film seen by neighbours
        for neighbor in knn[user]:
            for movie in urm[neighbor]:
                if movie not in urm[user]:
                    seen_movies.setdefault(movie, {}).setdefault(neighbor)
                    seen_movies[movie][neighbor] = urm[neighbor][movie]
        for movie in seen_movies:
            rankings.setdefault(movie, 0)
            sim_sums.setdefault(movie, 0)
            for neighbor in seen_movies[movie]:
                rankings[movie] += seen_movies[movie][neighbor]*knn[user][neighbor]
                sim_sums[movie] += knn[user][neighbor]
            rankings[movie] /= (sim_sums[movie] + shrink)
            recommendations.append((rankings[movie], movie))
            recommendations = sorted(recommendations, key=lambda x: -x[0])
            recommendations = recommendations[0:n]
        if len(recommendations) < n:
            for elem in avg_rec:
                recommendations.append(elem)

    else:
        recommendations = avg_rec

    recommendations = recommendations[0:n]
    rec = {}
    for (rating, movie) in recommendations:
        rec[movie] = rating
    return rec


def get_top_n_item_recommendations(movie_mat, urm, user, knn, n=5, shrink=10):
    """

    Parameters
    ----------
    movie_mat
    urm
    user
    knn
    n
    shrink

    Returns
    -------

    """
    scores = {}
    simSums = {}
    avg_rec = [(5.0, 33173), (5.0, 33475), (5.0, 1076), (5.0, 35300), (5.0, 15743)]
    for movie in urm[user]:
        if movie in knn:
            for other_movie in knn[movie]:
                if other_movie not in urm[user]:
                    simil = knn[movie][other_movie]
                    scores.setdefault(other_movie, 0.0)
                    scores[other_movie] += urm[user][movie]*simil
                    simSums.setdefault(other_movie, 0.0)
                    simSums[other_movie] += simil
        rankings = []
        for item in scores:
            rankings.append((float(scores[item] / (simSums[item] + shrink)), item))
        rec = sorted(rankings, key=lambda x: -x[0])[0:n]
        if len(rec) < n:
            for item in avg_rec:
                rec.append(item)
        return rec[0:n]

"""
Here we're building two different dictionaries
    * {userId: {movieId: rating}}
    * {movieId: {userId: rating}}
"""
urm = {}
movie_ratings = {}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    # create a nested dict; {userId: {movieId: rating}}
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]), {}).setdefault(int(row[1]))
            urm[int(row[0])][int(row[1])] = float(row[2])
            movie_ratings.setdefault(int(row[1]), {}).setdefault(int(row[0]))
            movie_ratings[int(row[1])][int(row[0])] = float(row[2])

print(top_n_match(movie_ratings, 1, skr=10, similarity=cosine_sim))
time = datetime.now()

movie_knn = {}
user_knn = {}
"""
with open('resources/test.csv') as test_raw:
    reader = csv.reader(test_raw)
    # create a nested dict for test user
    for row in reader:
        if row[0] != 'userId':
            user_knn[int(row[0])] = top_n_match(urm, int(row[0]), skr=10, n=20, similarity=cosine_sim)
            print('fatto user: ' + row[0])
"""
for movie in movie_ratings:
    movie_knn.setdefault(movie, {})
    movie_knn[movie] = top_n_match(movie_ratings, movie, skr=10, n=20, similarity=cosine_sim)
    print('fatto movie: ' + str(movie))
print(datetime.now() - time)

print(get_top_n_item_recommendations(movie_ratings, urm, 4, movie_knn))

"""user_rec = {}
for user in sorted(user_knn):
    user_rec[user] = get_top_n_recommendations(urm, user, user_knn, n=15, shrink=0)
    print('fatto: ' + str(user))
print(len(user_rec))
"""
"""
TODO: weighting the ratings!!!!!
"""










