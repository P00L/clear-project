import csv
import datetime
from similarity import item_sim


def cbf_recommendations(user_ratings, icm_m, sim_srk=20, shrink=10):
    """
    * WARNING:
        # This function is very resources and time consuming if it is done in large batch (e.g in a for loop over
        the whole movies)

    This function computes the recommendations using a CBF (Content Based Filtering) technique.

    Right now the implementation supports only a a fast similarity called item_sim (Doc in similarity.py)

    * NOTE:
        # this does not contain any optimization, it is just a simple and raw computation

    * TODO:
        # support for cosine
        # some optimization are needed

    Parameters
    ----------
    user_ratings: ratings of the user, it contains all the rated movie by an user
    icm_m: item content matrix
    sim_srk: shrink term f the similarity
    shrink: shrink of the function itself

    Returns
    -------
    A pre-formatted string containing the 5 best recommendations (NOTE: this has been done to be less time consuming)

    """
    totals = {}  # dizionario {item: sum (rating * similarity)}
    sim_sums = {}  # dizionario {item: sum (similarity)}

    for other_movie in icm_m:  # scandisco tutti i movie non recensiti dall'user e li confronto con quelli recensiti
        if other_movie not in user_ratings:
            for movie in user_ratings:
                if movie != other_movie:
                    # per ogni movie non recensito dall'user calcolo la similarity con quelli recensiti
                    similarity = item_sim(icm_m, movie, other_movie, skr=sim_srk)
                if similarity != 0:
                    totals.setdefault(other_movie, 0)
                    totals[other_movie] += user_ratings[movie]*similarity
                    sim_sums.setdefault(other_movie, 0)
                    sim_sums[other_movie] += similarity
    # shrink a caso ma sembra non cambiare molto tra uno o l'altro
    rankings = [(total/(sim_sums[item] + shrink), item) for item, total in totals.items()]
    sort_rankings = sorted(rankings, key=lambda x: -x[0])[0:5]
    string_s = ""
    for rate in range(0, len(sort_rankings)):
        string_s = string_s + " " + str(sort_rankings[rate][1])
    return string_s

icm = {}
urm = {}
dict_similarity = {}  # dizionario delle similarity del tipo {'(movie, other)' : 'sim'}
# icm --> {item:{feature:1}
with open('resources/icm.csv', 'r') as icm_raw:

    reader = csv.reader(icm_raw)
    for row in reader:
        if row[0] != 'itemId':
            icm.setdefault(int(row[0]), {}).setdefault(int(row[1]), 1)

# urm --> {user:{item:rating}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]), {})[int(row[1])] = int(row[2])


with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    user_test_list = list(reader)

"""
============================= NOTE =================================
if possible, to traceback the submission, rename the file in this way
 **********  cbf_srk_[shrink]_sim_[sim_srk].csv   *****************
====================================================================
"""
time = datetime.datetime.now()
with open('submission/cbf_srk_15_sim_25.csv', 'w', newline='') as f:
    my_dict = {}
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for i in range(1, len(user_test_list)):
        my_dict['userId'] = user_test_list[i][0]
        my_dict['testItems'] = cbf_recommendations(urm[int(user_test_list[i][0])], icm, shrink=15, sim_srk=25)
        w.writerow(my_dict)
        print(str(my_dict['userId']) + "," + str(my_dict['testItems']))
print(datetime.datetime.now() - time)
