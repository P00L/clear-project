import csv
import datetime
from similarity import cosine_sim, top_n_match


# item bias
item_bias = {}
with open('resources/item_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'ItemId':
            item_bias[int(row[0])] = float(row[1])

# user bias
user_bias = {}
with open('resources/user_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    i = 1
    for row in reader:
        if row[0] != 'UserId':
            user_bias[int(row[0])] = float(row[1])

# riempio user_bias e item_bias per fillare i valori mancanti
for i in range(1,15374):
    if i not in user_bias:
        user_bias[i] = float(0)

for i in range(1,37143):
    if i not in item_bias:
        item_bias[i] = float(0)

urm = {}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    # create a nested dict; {userId: {movieId: rating}}
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[1]), {}).setdefault(int(row[0]))
            urm[int(row[1])][int(row[0])] = float(row[2]) + item_bias[int(row[1])] + user_bias[int(row[0])]
print('computing right now')
time = datetime.datetime.now()
print(datetime.datetime.now() - time)

knn = {}
time = datetime.datetime.now()
"""
for movie in sorted(icm):
    knn[movie] = top_n_match(icm, movie, skr=5, n=25, similarity=item_sim)
    print('fatto movie: ' + str(movie))

print(len(knn))
"""
with open('resources/knn_movie_urm_25.csv', 'w') as knn_raw:
    fieldnames = ['itemId', 'neighborId', 'similarity']
    w = csv.DictWriter(knn_raw, fieldnames=fieldnames)
    w.writeheader()
    for movie in sorted(urm):
        knn[movie] = top_n_match(urm, movie, skr=5, n=25, similarity=cosine_sim)
        print('fatto movie: ' + str(movie))
        for other in knn[movie]:
            knn_raw.write(str(movie) + ',' + str(other) + ',' + str(knn[movie][other]) + '\n')
print(datetime.datetime.now() - time)