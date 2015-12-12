__author__ = 'paolo'
import csv
import random
from operator import itemgetter

with open('resources/train.csv', 'r') as urm:
    reader = csv.reader(urm)
    urm = {}
    for row in reader:
        if row[0]!= 'userId':
                urm.setdefault(int(row[0]),{})[int(row[1])]=int(row[2])


# aggiungiamo a urm_md  gli utenti con  voti >= 6 positivi (ovvero voti >=8)

urm_train = {}
for user in urm.keys():
    count = 0
    for item in urm[user]:
        if urm[user][item] >= 8:
            count += 1
    if count >= 6:
        urm_train[user] = urm[user]

# urm_train deve essere splittata in 20% che diventa test (random) e l'80% che rimane train

urm_test = {}
percentage = int(int((len(urm_train))*20)/100)

for key in random.sample(urm_train.keys(), percentage):
    urm_test[key] = urm_train[key]
    del urm_train[key]

# conto quanti volte un film e' stato votato usando un dizionario {'itemId':'numberOfRatings'} sull'intera urm


with open('resources/train.csv', 'rt') as f:
    reader = csv.reader(f)
    movie = {}
    for row in reader:
        if row[0] != 'userId':
            movie.setdefault(int(row[1]), []).append(row[2])

popularity = {}
for key in movie:
    popularity[key] = len(movie[key])

# ' dizionario che facciamo e' {'userId':{'itemId':'countItem'}}

urm_test_number_of_rating = {}
for user in urm_test:
    for item in urm_test[user]:
        urm_test_number_of_rating.setdefault(int(user), {}).setdefault(item, 0)
        urm_test_number_of_rating[user][item]=urm_test[user][item]

for user in urm_test_number_of_rating:
    for item in urm_test_number_of_rating[user]:
        if item in popularity:
            urm_test_number_of_rating[user][item] = popularity[item]

# 5 film meno popolari degli utenti con valori positivi rimangono nel test, e gli altri vanno a finire nel train
# per ogni utente di test devo ordinare urm_test_n_of_rating, prendere i meno popolari controllando se il rating e' >=8
# per i primi 5, e gli altri item finiranno nel set di train

print("urm:test: " + str(urm_test))
print("urm test pop;" + str(urm_test_number_of_rating))
for user in urm_test.keys():
    ordered_pop = sorted(urm_test_number_of_rating[user].items(), key=itemgetter(1))
    count = 0
    test_element = []
    for i in range(0, len(ordered_pop)):
        if urm_test[user][ordered_pop[i][0]] >= 8 and count != 5:
            test_element.append(ordered_pop[i][0])
            count += 1

    item_to_delete = []
    for item in urm_test[user]:
        if item not in test_element:
            urm_train.setdefault(user,{})[item]= urm_test[user][item]
            item_to_delete.append(item)

    for i in range(0, len(item_to_delete)):
        del urm_test[user][item_to_delete[i]]

'''
# FINALLY: dobbiamo togliere 80% dei dei rating dal train set
tot_ratings = 0
for user in urm_train.keys():
    tot_ratings += len(urm_train[user])

perc_ratings = int((tot_ratings*80)/100)
num_user = len(urm_train)

break_point = 0
for user in random.sample(urm_train.keys(), num_user):
    for item in random.sample(dict(urm_train[user]).keys(), len(urm_train[user])):
        if len(urm_train[user]) > 2:
            del urm_train[user][item]
        break_point += 1
        if break_point == perc_ratings: break
    if break_point == perc_ratings: break

tot_ratings = 0
for user in urm_train.keys():
    tot_ratings += len(urm_train[user])
'''
# Creiamo i csv tran e test

with open('test/train_split.csv', 'w',newline='') as f:  # Just use 'w' mode in 3.x
    my_dict = {}
    fieldnames = ['userId', 'itemId','rating']
    w = csv.DictWriter(f,fieldnames=fieldnames)
    w.writeheader()
    for user in urm_train:
        for item in urm_train[user]:
            my_dict['userId'] = user
            my_dict['itemId'] = item
            my_dict['rating'] = urm_train[user][item]
            w.writerow(my_dict)

with open('test/test_split.csv', 'w',newline='') as f:  # Just use 'w' mode in 3.x
    my_dict = {}
    fieldnames = ['userId', 'itemId','rating']
    w = csv.DictWriter(f,fieldnames=fieldnames)
    w.writeheader()
    for user in urm_test:
        for item in urm_test[user]:
            my_dict['userId'] = user
            my_dict['itemId'] = item
            my_dict['rating'] = urm_test[user][item]
            w.writerow(my_dict)
            print(my_dict)