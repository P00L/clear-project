import csv
import datetime
from math import sqrt

def similarity_fast(icm, item1, item2):
    if item1 not in icm or item2 not in icm:
        return 0
    shared = 0
    for val in icm[item1]:
        if val in icm[item2]:
            shared += 1
    num = shared
    den = len(icm[item2]) + len(icm[item1]) - shared + 20

    return round(num/den, 3)

#versione senza dizionario che si satura troppo presto
def cbf_recommendations(user_ratings, icm_m):
    totals = {} #dizionario {item: sum (rating * similarity)}
    sim_sums = {} #dizionario {item: sum (similarity)}

    for other_movie in icm_m:# scandisco tutti i movie non recensiti dall'user e li confronto con quelli recensiti
        if other_movie not in user_ratings:
            for movie in user_ratings:
                if movie != other_movie:
                    similarity = similarity_fast(icm_m, movie, other_movie)#per ogni movie non recensito dall'user calcolo la similarity con quelli recensiti
                if similarity != 0:
                    totals.setdefault(other_movie, 0)
                    totals[other_movie] += user_ratings[movie]*similarity
                    sim_sums.setdefault(other_movie, 0)
                    sim_sums[other_movie] += similarity
    # shrink a caso ma sembra non cambiare molto tra uno o l'altro
    rankings = [(total/(sim_sums[item]+10), item) for item, total in totals.items()]
    sort_rankings = sorted(rankings, key=lambda x: -x[0])[0:5]
    stringami = ""
    for rate in range(0,len(sort_rankings)):
        stringami = stringami + " " + str(sort_rankings[rate][1])
    return stringami

icm = {}
urm = {}
dict_similarity = {} #dizionario delle similarity del tipo {'(movie, other)' : 'sim'}
#icm --> {item:{feature:1}
with open('E:/Polimi/Recommender system/challenge/icm.csv', 'r') as icm_raw:

    reader = csv.reader(icm_raw)
    for row in reader:
        if row[0] != 'itemId':
            icm.setdefault(int(row[0]), {}).setdefault(int(row[1]), 1)

#urm --> {user:{item:rating}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]), {})[int(row[1])] = int(row[2])



with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    user_test_list = list(reader)

with open('submission/cbf_skr20_10.csv', 'w',newline='') as f:
    my_dict = {}
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(f,fieldnames=fieldnames)
    w.writeheader()
    for i in range(1, len(user_test_list)):
        my_dict['userId'] = user_test_list[i][0]
        my_dict['testItems'] = cbf_recommendations(urm[int(user_test_list[i][0])], icm)
        w.writerow(my_dict)
        print(str(my_dict['userId']) + "," +str(my_dict['testItems']))