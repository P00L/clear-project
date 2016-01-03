import csv

urm = {}  # {user : {item:rating}
movie = {}  # {item : [lista di voti]}
item_bias = {} # {item : bias}
user_bias = {} # {user : bias}
item_avg = {}   # {item : avg rating}
popularity = [] # [(item , numero voti)]
popularity_dict = {} # {item : numero voti}
index_pop = {} # {item : indice posizione popularity} serve per velocizzare l'eliminazione dei film
user_min_pop = {} # {user : min_pop}


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

# filliamo item avg con gli item mancanti con media 0
for i in range(1,37143):
    if i not in item_avg:
        item_avg[i] = float(0)

# prepariamo il necessario per togliere le cose troppo popolari mirate
for item in movie:
    popularity.append((item, len(movie[item])))
    popularity_dict[int(item)] = len(movie[item])
# filliamo i film mancanti con popolarita 0
for i in range(1,37143):
    if i not in movie:
        popularity.append((i , 0))
# ordiniamo i film per popolarita' max-->min
sort_popularity = sorted(popularity, key=lambda x: -x[1])
# riempiamo index_pop
indice = 0
prev = 999999
for f in sort_popularity:
    if prev != f[1]:
        index_pop[f[1]] = indice
        prev = f[1]
    indice += 1
# riempiamo user_min_pop con la minima popolarita'
for user in urm:
    min = 37143
    for item in urm[user]:
        if popularity_dict[item] < min:
           min =  popularity_dict[item]
    user_min_pop[user] = min
# filliamo i valori mancanti di user(forse non serve)
for i in range(0,15374):
    if i not in user_min_pop:
        user_min_pop[i] = 0
print(sort_popularity)
print(index_pop[78])
for item in urm[10]:
    print("film "+str(item)+" popularity "+str(popularity_dict[item]))
print("min popo "+str(user_min_pop[10]))

