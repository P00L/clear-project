import csv
import datetime
from similarity import item_sim, cosine_sim


def cbf_hybrid_recommendations(user_ratings,user, icm_m, movies, sim_skr=20, shrink=10, w_urm=1.0, w_icm=1.0):
    """
    * WARNING:
        # This function is very resources and time consuming if it is done in large batch (e.g in a for loop over
        the whole movies)

    This function computes the recommendations using a CBF (Content Based Filtering) technique.

    Right now the implementation supports only a a fast similarity_icm called item_sim (Doc in similarity_icm.py)

    * NOTE:
        # this does not contain any optimization, it is just a simple and raw computation

    * TODO:
        # support for cosine
        # some optimization are needed

    Parameters
    ----------
    user_ratings: ratings of the user, it contains all the rated movie by an user
    icm_m: item content matrix
    sim_skr: shrink term f the similarity_icm
    shrink: shrink of the function itself

    Returns
    -------
    A pre-formatted string containing the 5 best recommendations (NOTE: this has been done to be less time consuming)

    """
    totals = {}  # dizionario {item: sum (rating * similarity_icm)}
    sim_sums = {}  # dizionario {item: sum (similarity_icm)}
    avg_rec = [(5.0, 33173), (5.0, 33475), (5.0, 1076), (5.0, 35300), (5.0, 15743)]

    for other_movie in icm_m:  # scandisco tutti i movie non recensiti dall'user e li confronto con quelli recensiti
        if other_movie not in user_ratings:
            for movie in user_ratings:
                if movie != other_movie:
                    # per ogni movie non recensito dall'user calcolo la similarity_icm con quelli recensiti
                    similarity_icm = item_sim(icm_m, movie, other_movie, skr=sim_skr)
                    similarity_urm = cosine_sim(movies, movie, other_movie, skr=6)
                if similarity_icm != 0 or similarity_urm != 0:
                    totals.setdefault(other_movie, 0)
                    #totals[other_movie] += user_ratings[movie]*similarity_icm + avg + user_bias[user] + item_bias[movie
                    totals[other_movie] += (w_icm*(user_ratings[movie]*similarity_icm) + w_urm*(user_ratings[movie]*similarity_urm))/(w_urm+w_icm)
                    sim_sums.setdefault(other_movie, 0)
                    sim_sums[other_movie] += (similarity_icm*w_icm + similarity_urm*w_urm)/(w_urm+w_icm)
    # compute the ranking for every movie, but the due to the shrink term the value are not prediction
    rankings = [(total/(sim_sums[item] + shrink), item) for item, total in totals.items()]
    sort_rankings = sorted(rankings, key=lambda x: -x[0])[0:5]
    # This should happen when there are less than five similar movie for the movies
    if len(sort_rankings) < 5:
        for elem in avg_rec:
            sort_rankings.append(elem)
    sort_rankings = sort_rankings[0:5]
    string_s = ""
    for rate in range(0, len(sort_rankings)):
        string_s = string_s + " " + str(sort_rankings[rate][1])
    return string_s

icm = {}
urm = {}
movies = {}
dict_similarity = {}  # dizionario delle similarity del tipo {'(movie, other)' : 'sim'}
# icm --> {item:{feature:1}
with open('resources/icm.csv', 'r') as icm_raw:

    reader = csv.reader(icm_raw)
    for row in reader:
        if row[0] != 'itemId':
            icm.setdefault(int(row[0]), {}).setdefault(int(row[1]), 1)

#item bias
item_bias = {}
with open('resources/item_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'ItemId':
            item_bias[int(row[0])] = float(row[1])

#user bias
user_bias = {}
with open('resources/user_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    i = 1
    for row in reader:
        if row[0] != 'UserId':
            user_bias[int(row[0])] = float(row[1])

#riempio user_bias e item_bias per fillare i valori mancanti
for i in range(1,15374):
    if i not in user_bias:
        user_bias[i] = float(0)

for i in range(1,37143):
    if i not in item_bias:
        item_bias[i] = float(0)

for i in range(1,37143):
    if i not in movies:
        movies.setdefault(i, {})

# urm --> {user:{item:rating}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]), {})[int(row[1])] = round(float(row[2])+user_bias[int(row[0])]+item_bias[int(row[1])], 5)
            movies.setdefault(int(row[1]), {})[int(row[0])] = round(float(row[2])+user_bias[int(row[0])]+item_bias[int(row[1])], 5)



with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    user_test_list = list(reader)

"""
=============================== NOTE ==================================
if possible, to traceback the submission, rename the file in this way
 **********  cbf_srk[sim_skr]sim_skr[sim_srk]rank.csv   ***************
=======================================================================
"""
time = datetime.datetime.now()
print(cosine_sim(movies,1,7,))
with open('submission/cbf_hybrid_srk20simIcm_skr6simUrm_skr10rank_w0.333urm_w0.667icm.csv', 'w', newline='') as f:
    my_dict = {}
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for i in range(1, len(user_test_list)):
        my_dict['userId'] = user_test_list[i][0]
        my_dict['testItems'] = cbf_hybrid_recommendations(urm[int(user_test_list[i][0])],int(user_test_list[i][0]), icm, movies, shrink=10, sim_skr=20, w_urm=0.333, w_icm=0.667)
        w.writerow(my_dict)
        print(str(my_dict['userId']) + "," + str(my_dict['testItems']))
print(datetime.datetime.now() - time)
