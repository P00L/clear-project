import csv
from datetime import datetime

__author__ = 'Alessandro'


def rec_to_string(lst):
    """
    This functions simply returns a formatted version of the list of recommendations to print thi out

    :param lst: list of recommendations

    :return a formatted string like 'movieId movieId....'

    """
    string = ''
    for elem in lst:
        string += str(elem[0]) + ' '
    return string


def top_n_rec_knn_item(urm, knn, user, n=5, shrink=5):
    scores = {}
    avg_rec = [(33173, 5.0), (33475, 5.0), (1076, 5.0), (35300, 5.0), (15743, 5.0)]
    for movie in urm[user]:
        if movie in knn:
            for other_movie in knn[movie]:
                if other_movie in urm[user]:
                    continue
                sim = knn[movie][other_movie]
                scores.setdefault(other_movie, 0.0)
                scores[other_movie] += urm[user][movie] * sim

    rankings = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if len(rankings) < n:
        for item in avg_rec:
            rankings.append(item)

    return rankings[0:n]

knn = {}
with open('resources/knn_item_movie_25.csv', 'r')as knn_raw:
    reader = csv.reader(knn_raw)
    for row in reader:
        if row[0] != 'itemId':
            knn.setdefault(int(row[0]), {}).setdefault(int(row[1]))
            knn[int(row[0])][int(row[1])] = float(row[2])

urm = {}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    # create a nested dict; {userId: {movieId: rating}}
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]), {}).setdefault(int(row[1]))
            urm[int(row[0])][int(row[1])] = float(row[2])


test = {}
with open('resources/test.csv', 'r') as test_raw:
    reader = csv.reader(test_raw)
    # create a nested dict for test user
    for row in reader:
        if row[0] != 'userId':
            test.setdefault(int(row[0]))

time = datetime.now()
with open('submission/knn-item-25.csv', 'w') as sub_write:
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(sub_write, fieldnames=fieldnames)
    w.writeheader()
    for user in sorted(test):
        rec = top_n_rec_knn_item(urm, knn, user)
        sub_write.write(str(user) + ',' + rec_to_string(rec) + '\n')
        print('user %S done', user)
print(datetime.now() - time)