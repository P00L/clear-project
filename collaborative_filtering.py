import csv
from math import sqrt

def squared_root(x):
    return round(sqrt((sum([(x[val] - item_avg[val]) * (x[val] - item_avg[val]) for val in x]))), 3)

#FORSE NON E ADJUSTED COSINE MA PEARSON
def adj_cosine_sim(urm, user1, user2, skr=0.0):
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


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(urm,person, skr):

    totals={}
    for other in urm:
        # don't compare me to myself
        if other==person: continue
        sim=adj_cosine_sim(urm,person,other, skr)
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in urm[other]:
            #only score movies I haven't seen yet
            if item not in urm[person] or urm[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=urm[other][item] * sim

    #togliamo da totals i film troppo popolari
    for i in range(0,1500):
        if sort_popularity[i][0]in totals:
            del totals[sort_popularity[i][0]]

    # Create the normalized list
    rankings=[(total,item) for item,total in totals.items( )]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()

    rankings_cut = []
    if len(rankings)> 5:
        rankings_cut = rankings[0:5]
    result = ""
    avg_rating = ['33173' , '33475', '1076','15743','35300']
    for i in range(len(rankings_cut)):
        result = result + " " + str(rankings_cut[i][1])
    for i in range(5 - len(rankings_cut)):
        result = result + " " + avg_rating[i]

    return result

item_bias = {}
user_bias = {}
urm = {}
item_avg = {}
movie = {}  #movie {item:numero voti} serve per la popularity

with open('resources/item_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'ItemId':
            item_bias[int(row[0])] = float(row[1])

with open('resources/user_bias.csv', 'rt') as f:
    reader = csv.reader(f)
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

with open('resources/item_avg.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'ItemId':
            item_avg[int(row[0])] = float(row[1])

for i in range(1,37143):
    if i not in item_avg:
        item_avg[i] = float(0)


#{user:{item:rating}}  gli indici e i value sono user= int item 0 int rating = float
with open('resources/train.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0]!= 'userId':
                urm.setdefault(int(row[0]),{})[int(row[1])]=round(float(row[2])+user_bias[int(row[0])]+item_bias[int(row[1])], 5)


with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    test_dict = {}
    for row in reader:
        if row[0] != "userId":
            test_dict.setdefault(int(row[0]))

with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    list = list(reader)


with open('resources/train.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'userId':
            movie.setdefault(int(row[1]), []).append(row[2])

popularity = []
for key in movie:
    popularity.append((key,len(movie[key])))

sort_popularity = sorted(popularity, key=lambda x: -x[1])
print(sort_popularity[0:1000])

with open('submission/cf_AdjCosine_skr6cosine_bias_noDenRanking_popularity1500.csv', 'w',newline='') as f:  # Just use 'w' mode in 3.x
    my_dict = {}
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(f,fieldnames=fieldnames)
    w.writeheader()
    for i in range(1, len(list)):
        my_dict['userId'] = list[i][0]
        my_dict['testItems'] = getRecommendations(urm, int(list[i][0]), 6)
        w.writerow(my_dict)
        print(my_dict)