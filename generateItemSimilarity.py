__author__ = 'Federica'

import csv
import similarity

#{user:{item:rating}}  gli indici e i value sono user= int item 0 int rating = float
with open('resources/train.csv', 'rt') as f:
    reader = csv.reader(f)
    urm = {}
    for row in reader:
        if row[0]!= 'userId':
                urm.setdefault(int(row[0]),{})[int(row[1])]=float(row[2])

#switcha gli item con le persone che li hanno votati {'item':{'user':ranking}}
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person]=prefs[person][item]
    return result

# questa calcola tutti gli item simili tra di loro
def calculateSimilarItems(prefs,n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result={}
    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        # Status updates for large datasets
        c+=1
        if c%100==0: print ("%d / %d" % (c,len(itemPrefs)))
        # Find the most similar items to this one
        scores=topMatches(itemPrefs, item, n=n, similarity=similarity.cosine_sim)
        result[item]=scores
    return result


#Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=similarity.cosine_sim):
    scores=[(similarity(prefs,person,other,2),other)
        for other in prefs if other!=person]
# Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]


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

with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    test_dict = {}
    for row in reader:
        if row[0] != "userId":
            test_dict.setdefault(int(row[0]))

with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    list = list(reader)

with open('resources/item_similarity1.csv', 'w',newline='') as f:  # Just use 'w' mode in 3.x
    my_dict = {}
    # item_dict e' un dizionario fatto come {'item':{'item':similarity}}
    item_dict = calculateSimilarItems(urm)
    fieldnames = ['item1','item2','sim']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for item1 in item_dict:
        for  item2 in item_dict[item1]:
            my_dict['item1']= item1
            my_dict['item2'] = item2[1]
            my_dict['sim'] = item2[0]
            w.writerow(my_dict)
            print(my_dict)