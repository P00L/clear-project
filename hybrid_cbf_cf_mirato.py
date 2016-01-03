import csv
import datetime
from similarity import item_sim, cosine_sim
from math import sqrt


def adj_cosine_sim(urm, user1, user2, skr=0.0):
    """
    adjusted cosine ? or  pearson?
    Parameters
    ----------
    urm: urm matrix
    user1: the first user
    user2: the user to be compared with
    skr: the shrink factor

    Returns
    -------
    Float that represents similarity between two users

    """
    shared_1 = {}
    shared_2 = {}
    for val in urm[user1]:
        if val in urm[user2]:
            shared_1[val] = urm[user1][val]
            shared_2[val] = urm[user2][val]
    if len(shared_1) == 0:
        return 0
    num = sum([(shared_1[val] - item_avg[val]) * (shared_2[val] - item_avg[val]) for val in shared_1])
    den = squared_root(urm[user1])*squared_root(urm[user2])
    return round(num/(den + skr), 3)


def squared_root(x):
    return round(sqrt((sum([(x[val] - item_avg[val]) * (x[val] - item_avg[val]) for val in x]))), 3)


def hybrid_rec(user_ratings, user, icm_m, sim_skr=20, w_cbf=0.87, w_cf=0.13):
    """
    hybrid recommendations for a user
    Parameters
    ----------
    user_ratings: the rating of the user to be recommended
    user: the user to be recommenended
    icm_m: the ICM matrix
    sim_skr: the shrink sim for CBF
    w_cbf: the weight for CBF
    w_cf: the weight for CF

    Returns
    -------
    List of 5 movies recommended
    """
    totals_cbf = {}  #{item : sum (rating * similarity)}
    totals_cf = {}  #{item : sum (rating * similarity)}
    rankings = {}   #{item : (sim_cbf * w_cbf) + (sim_cf * w_cf)}
    avg_rec = [(5.0, 33173), (5.0, 33475), (5.0, 1076), (5.0, 35300), (5.0, 15743)]

    # generiamo il ranking di cbf
    for other_movie in icm_m:  # scandisco tutti i movie non recensiti dall'user e li confronto con quelli recensiti
        if other_movie not in user_ratings:
            for movie in user_ratings:
                if movie != other_movie:
                    # per ogni movie non recensito dall'user calcolo la similarity con quelli recensiti
                    similarity = item_sim(icm_m, movie, other_movie, skr=sim_skr)
                if similarity != 0:
                    totals_cbf.setdefault(other_movie, 0.0)
                    totals_cbf[other_movie] += user_ratings[movie]*similarity

    # generiamo il ranking di cf
    for other in urm:
        # don't compare me to myself
        if other==user: continue
        similarity_urm = adj_cosine_sim(urm,user,other,6)
        # ignore scores of zero or lower
        if similarity_urm <= 0 : continue
        for item in urm[other]:
            # only score movies I haven't seen yet
            if item not in urm[user] or urm[user][item]==0:
                # Similarity * Score
                totals_cf.setdefault(item,0)
                totals_cf[item] += urm[other][item]*similarity_urm

    # mergiamo i ranking di cbf e cf pesando i valori
    for movie in totals_cbf:
        rankings[movie] = totals_cbf[movie]*w_cbf
        if movie in totals_cf:
            rankings[movie] += totals_cf[movie]*w_cf
    for movie in totals_cf:
        if movie not in rankings:
            rankings[movie] = totals_cf[movie]*w_cf

    # togliamo da ranking i movie troppo popolari
    # se il film meno popolare votato dall'user ha meno di 10 voti metto una soglia nel range dove eliminare
    if user_min_pop[user] < 10:
        for i in range(0, index_pop[(user_min_pop[user] + 5)]):
            if sort_popularity[i][0]in rankings:
                del rankings[sort_popularity[i][0]]
    # altrimenti eliminiamo i film piu' popolari del meno popolare votato dall'utente senza nessuna soglia
    else:
        for i in range(0,index_pop[user_min_pop[user]]):
            if sort_popularity[i][0]in rankings:
                del rankings[sort_popularity[i][0]]

    """
    for i in range(0,index_pop[user_min_pop[user]]):
        if sort_popularity[i][0]in rankings:
            del rankings[sort_popularity[i][0]]
    """
    # compute the ranking for every movie, but the due to the shrink term the value are not prediction
    rankings_final = [(total, item) for item, total in rankings.items()]
    sort_rankings = sorted(rankings_final, key=lambda x: -x[0])[0:5]
    # This should happen when there are less than five similar movie for the movies
    if len(sort_rankings) < 5:
        for elem in avg_rec:
            sort_rankings.append(elem)
    sort_rankings = sort_rankings[0:5]
    string_s = ""
    for rate in range(0, len(sort_rankings)):
        string_s = string_s + " " + str(sort_rankings[rate][1])
    return string_s

icm = {}  # {item : {feature : 1}
urm = {}  # {user : {item : rating}
movie = {}  # {item : [lista di voti]}
item_bias = {} # {item : item_bias}
user_bias = {} # {user : user_bias}
item_avg = {}   # {item : avg_rating}
popularity = [] # [(item , numero voti)]  ----> lista di tuple per avere l'ordinamento sulla popolarita
popularity_dict = {} # {item : numero voti}
index_pop = {} # {numero voti : indice posizione in popularity} serve per velocizzare l'eliminazione dei film salvando la PRIMA occorrenza del valore di popolarita'
user_min_pop = {} # {user : minimo numero voti}

# apriamo la icm
with open('resources/icm.csv', 'r') as icm_raw:
    reader = csv.reader(icm_raw)
    for row in reader:
        if row[0] != 'itemId':
            icm.setdefault(int(row[0]), {}).setdefault(int(row[1]), 1)

# apriamo gli item bias
with open('resources/item_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'ItemId':
            item_bias[int(row[0])] = float(row[1])

# apriamo gli user bias
with open('resources/user_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'UserId':
            user_bias[int(row[0])] = float(row[1])

# riempiamo user_bias e item_bias per fillare i valori mancanti
for i in range(1,15374):
    if i not in user_bias:
        user_bias[i] = float(0)
for i in range(1,37143):
    if i not in item_bias:
        item_bias[i] = float(0)

# apriamo la urm in tutti i modi che ci serve
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]), {})[int(row[1])] = round(float(row[2])+user_bias[int(row[0])]+item_bias[int(row[1])], 5)
            movie.setdefault(int(row[1]), []).append(row[2])

# apriamo gli user di test per cui calcolare le predizioni
with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    user_test_list = list(reader)

# apriamo item avg
with open('resources/item_avg.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'ItemId':
            item_avg[int(row[0])] = float(row[1])

# riempiamo item avg con gli item mancanti con media 0
for i in range(1,37143):
    if i not in item_avg:
        item_avg[i] = float(0)

# prepariamo il necessario per togliere le gli item piu' popolari del meno popolare votato da ogni user
for item in movie:
    popularity.append((item, len(movie[item])))
    popularity_dict[int(item)] = len(movie[item])
# riempiamo i film mancanti con popolarita' 0
for i in range(1,37143):
    if i not in movie:
        popularity.append((i , 0))
# ordiniamo i film per popolarita' max-->min
sort_popularity = sorted(popularity, key=lambda x: -x[1])
# riempiamo index_pop con l'occorrenza del primo valore di popolarita'
indice = 0
prev_pop = 999999 # un valore alto sicuramente diverso da qualsiasi valore di popolarita
for f in sort_popularity:
    if prev_pop != f[1]:
        index_pop[f[1]] = indice
        prev_pop = f[1]
    indice += 1
# riempiamo user_min_pop con la minima popolarita' tra i film votati dall'utente
for user in urm:
    min = 37143
    for item in urm[user]:
        if popularity_dict[item] < min:
           min =  popularity_dict[item]
    user_min_pop[user] = min
# riempiamo i valori mancanti di user(forse non serve)
for i in range(0,15374):
    if i not in user_min_pop:
        user_min_pop[i] = 0

# qui si fa tutto
time = datetime.datetime.now()
with open('submission/hybrid_cbf_cfAdjCosine_w0.13cf_w0.87cbf_mira_soglia5.csv', 'w', newline='') as f:
    my_dict = {}
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for i in range(1, len(user_test_list)):
        my_dict['userId'] = user_test_list[i][0]
        my_dict['testItems'] = hybrid_rec(urm[int(user_test_list[i][0])], int(user_test_list[i][0]), icm, sim_skr=20)
        w.writerow(my_dict)
        print(str(my_dict['userId']) + "," + str(my_dict['testItems']))
print(datetime.datetime.now() - time)