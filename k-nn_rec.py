import csv
from datetime import datetime
from builtins import print
__author__ = 'Alessandro'


def rec_to_string(lst):
    """
    This functions simply returns a formatted version of the list of recommendations to print thi out

    :param lst: list of recommendations

    :return a formatted string like 'movieId movieId....'

    """
    string = ''
    for elem in lst:
        string += str(elem[1]) + ' '
    return string


def usr_avg(user_ratings):
    """
    compute the average rating for a user

    :param user_ratings: the ratings of an user (the form should be urm[user]

    :return: rounded float (x.yzk) that is the average rating of that user
    """
    return round(sum(user_ratings[movie] for movie in user_ratings) / len(user_ratings), 3)


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

    return recommendations[0:n]


def top_n_with_global_effect(urm, user, knn, n=5, shrink=10):
    """
    * TODO:
        # check if the code is correct or not
        # check if with different value in this shrink or in the cosine shrink gives better score

    Compute the top_n_match with k-NN and moreover it should count about the global effect, e.g. the mean rating of any
    user in order to get better recommendations

    * SCORING:
        right now this technique seems to score less than the base one (102 with shrink 10 on the same k-NN data set)

    :param urm: user rating matrix
    :param user: the user i want recommendations
    :param knn: the k-NN dictionary
    :param n: num of recommendations
    :param shrink: the shrinkage

    :return: a list of tuples (value, movieId) containing the recommendations
    """
    avg_rec = [(5.0, 33173), (5.0, 33475), (5.0, 1076), (5.0, 35300), (5.0, 15743)]
    seen_movies = {}
    rankings = {}
    sim_sums = {}
    recommendations = []
    user_avg = usr_avg(urm[user])
    # otherwise i cannot apply this formula
    if user in knn:
        for neighbor in knn[user]:
            for movie in urm[neighbor]:
                if movie not in urm[user]:
                    seen_movies.setdefault(movie, {}).setdefault(neighbor)
                    seen_movies[movie][neighbor] = urm[neighbor][movie]
        for movie in seen_movies:
            rankings.setdefault(movie, 0)
            sim_sums.setdefault(movie, 0)
            for neighbor in seen_movies[movie]:
                # a single rank is in the form (rating - average of neighbor) * similarity
                rankings[movie] += (seen_movies[movie][neighbor] - usr_avg(urm[neighbor]))*knn[user][neighbor]
                sim_sums[movie] += knn[user][neighbor]
            # here come the shrinkage
            rankings[movie] /= (sim_sums[movie] + shrink)
            """
            add the user rating to get a quasi-realistic rating --> quasi means if th shrink is too much the rating
            cannot be predicted but i can extract only recommendations
            """
            rankings[movie] += user_avg
            recommendations.append((rankings[movie], movie))
            recommendations = sorted(recommendations, key=lambda x: -x[0])
            recommendations = recommendations[0:n]
        # if the length of recommendations is short i fill it with best average ratings
        if len(recommendations) < n:
            for elem in avg_rec:
                recommendations.append(elem)
    else:
        """
        i dunno anything 'bout the user.... it has no neighbor, so i cannot use this method, so i fill with the best movie
        for avg_rating
        """
        recommendations = avg_rec

    return recommendations[0:n]

"""
======================================== WARNING ============================================
Before running this script, you should already have the k-NN data set in the resources folder
=============================================================================================
"""
# ================ here starts the script========================
urm = {}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    # create a nested dict; {userId: {movieId: rating}}
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]), {}).setdefault(int(row[1]))
            urm[int(row[0])][int(row[1])] = float(row[2])

knn = {}
time = datetime.now()
"""
=========== WARNING!!! =============
THE FILE TO BE OPENED SHOULD BE
k-nn_[similarity]_user_[shrink]
====================================
"""
with open('resources/k-nn_cosine_user_15.csv', 'r') as knn_raw:
    reader = csv.reader(knn_raw)
    # create a nested dict for test user
    for row in reader:
        if row[0] != 'userId':
            knn.setdefault(int(row[0]), {}).setdefault(int(row[1]))
            knn[int(row[0])][int(row[1])] = float(row[2])
print(len(knn))
print(datetime.now() - time)

test = {}
with open('resources/test.csv', 'r') as test_raw:
    reader = csv.reader(test_raw)
    # create a nested dict for test user
    for row in reader:
        if row[0] != 'userId':
            test.setdefault(int(row[0]))

time = datetime.now()
"""
IMPORTANT!!!! -----> In order to traceback the results, if you can, submit this kind of file as
---------------------- knn-rec-[shrink].csv -----------------------
"""
with open('submission/knn-rec-15.csv', 'w') as sub_write:
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(sub_write, fieldnames=fieldnames)
    w.writeheader()
    for user in sorted(test):
        rec = get_top_n_recommendations(urm, user, knn, shrink=15)
        sub_write.write(str(user) + ',' + rec_to_string(rec) + '\n')
        print('user %S done', user)
print(datetime.now() - time)


