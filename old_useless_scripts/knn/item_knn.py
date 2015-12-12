import csv
import datetime
from similarity import cosine_sim, item_sim, top_n_match

icm = {}
with open('resources/icm.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    # create a nested dict; {userId: {movieId: rating}}
    for row in reader:
        if row[0] != 'itemId':
            icm.setdefault(int(row[0]), {}).setdefault(int(row[1]))
            icm[int(row[0])][int(row[1])] = 1
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
with open('resources/knn_item_movie_25.csv', 'w') as knn_raw:
    fieldnames = ['itemId', 'neighborId', 'similarity']
    w = csv.DictWriter(knn_raw, fieldnames=fieldnames)
    w.writeheader()
    for movie in sorted(icm):
        knn[movie] = top_n_match(icm, movie, skr=5, n=25, similarity=item_sim)
        print('fatto movie: ' + str(movie))
        for other in knn[movie]:
            knn_raw.write(str(movie) + ',' + str(other) + ',' + str(knn[movie][other]) + '\n')
print(datetime.datetime.now() - time)