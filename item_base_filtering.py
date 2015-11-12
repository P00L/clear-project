__author__ = 'Federica'
import csv
import similarity

#{user:{item:rating}}  gli indici e i value sono user= int item 0 int rating = float
with open('resources/train.csv', 'rt') as f:
    reader = csv.reader(f)
    urm = {}
    for row in reader:
        if row[0]!= 'userId':
                urm.setdefault(row[0], {})[row[1]]=float(row[2])

with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    test_dict = {}
    for row in reader:
        if row[0] != "userId":
            test_dict.setdefault(row[0])

with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    list = list(reader)

# item_dict deve essere fatto cosi': {'item': [('sim','item')]} un dizionario di lista di tuple
with open('resources/item_similarity.csv', 'rt') as f:
    reader = csv.reader(f)
    item_dict = {}
    for row in reader:
        if row[0]!='item1':
            item_dict.setdefault(row[0],[]).append((float(row[2]), row[1]))

def getRecommendedItems(prefs,itemMatch,user,sink):
    userRatings=prefs[user]
    scores={}
    totalSim={}

    # Loop over items rated by this user
    for (item,rating) in userRatings.items( ):

        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:

            # Ignore if this user has already rated this item
            if item2 in userRatings: continue

            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    # Divide each total score by total weighting to get an average
    rankings=[((score/totalSim[item]+sink),item) for item,score in scores.items()]

    # Return the rankings from highest to lowest
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


with open('submission/item_base_filtering_skr6.csv', 'w', newline='') as f:  # Just use 'w' mode in 3.x
    my_dict = {}
    #item_dict e' un dizionario fatto come {'item':{'item':similarity}}
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(f,fieldnames=fieldnames)
    w.writeheader()
    print(list)
    for i in range(1, len(list)):
        my_dict['userId'] = list[i][0]
        my_dict['testItems'] = getRecommendedItems(urm, item_dict, list[i][0], 6)
        w.writerow(my_dict)
