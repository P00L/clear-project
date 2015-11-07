import csv
from math import sqrt

#{user:{item:rating}}  gli indici e i value sono user= int item 0 int rating = float
with open('resources/train.csv', 'rt') as f:
    reader = csv.reader(f)
    urm = {}
    for row in reader:
        if row[0]!= 'userId':
                urm.setdefault(int(row[0]),{})[int(row[1])]=float(row[2])

#funzione che restituisce la similarita tra due user
def similarity_distance(urm,user_1,user_2):
    # Get the list of shared_items
    si={}
    for item in urm[user_1]:
        if item in urm[user_2]:
            si[item]=1
    # if they have no ratings in common, return 0
    if len(si)==0: return 0
    # Add up the squares of all the differences
    sum_of_squares=sum([pow(urm[user_1][item]-urm[user_2][item],2)
        for item in urm[user_1] if item in urm[user_2]])
    return 1/(1+sum_of_squares)


# funzione che restituisce la similarity tra due user con paerson
def similarity_pearson(urm, user_1, user_2, skr):
    # Get the list of mutually rated items
    si={}
    for item in urm[user_1]:
        if item in urm[user_2]: si[item]=1

    # Find the number of elements
    n=len(si)
    # if they are no ratings in common, return 0
    if n==0: return 0
    # Add up all the preferences
    sum1=sum([urm[user_1][it] for it in si])
    sum2=sum([urm[user_2][it] for it in si])
    # Sum up the squares
    sum1Sq=sum([pow(urm[user_1][it],2) for it in si])
    sum2Sq=sum([pow(urm[user_2][it],2) for it in si])
    # Sum up the products
    pSum=sum([urm[user_1][it]*urm[user_2][it] for it in si])
    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=(sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))+skr)
    if den==0: return 0

    r=num/den

    return r


def squared_root(x):
    return round(sqrt((sum([x[val] * x[val] for val in x]))), 3)

#shared e un dizionario di itme in comune {item:rating}
def similarity_cosine(urm, user1, user2, skr):
    shared_1 = {}
    shared_2 = {}
    for val in urm[user1]:
        if val in urm[user2]:
            shared_1[val] = urm[user1][val]
            shared_2[val] = urm[user2][val]
    #se non hanno niente in comune
    if len(shared_1) == 0:
        return 0
    num = sum([shared_1[val]*shared_2[val] for val in shared_1])
    den = (squared_root(urm[user1])*squared_root(urm[user2])+skr)
    return round(num/den, 3)


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,person):
    scores=[(similarity_distance(prefs,person,other),other)
                for other in prefs if other!=person]
    # Sort the list so the highest scores appear at the top
    scores.sort( )
    scores.reverse( )
    return scores[0:5]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person, skr):

    totals={}
    simSums={}
    for other in prefs:
        # don't compare me to myself
        if other==person: continue
        sim=similarity_pearson(prefs,person,other, skr)
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
            #only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    # Create the normalized list
    rankings=[(total/(simSums[item]+ skr),item) for item,total in totals.items( )]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()

    #Chiama cosine se le pearson fa schifo
    if len(rankings) == 0:
        totals={}
        simSums={}
        for other in prefs:
            # don't compare me to myself
            if other==person: continue
            sim=similarity_cosine(prefs,person,other, skr)
            # ignore scores of zero or lower
            if sim<=0: continue
            for item in prefs[other]:
                #only score movies I haven't seen yet
                if item not in prefs[person] or prefs[person][item]==0:
                    # Similarity * Score
                    totals.setdefault(item,0)
                    totals[item]+=prefs[other][item]*sim
                    # Sum of similarities
                    simSums.setdefault(item,0)
                    simSums[item] += sim
        # Create the normalized list
        rankings=[(total/(simSums[item]+skr),item) for item,total in totals.items( )]
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

with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    test_dict = {}
    for row in reader:
        if row[0] != "userId":
            test_dict.setdefault(int(row[0]))

with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    list = list(reader)

with open('submission/consegna_cb_pearson.csv', 'w',newline='') as f:  # Just use 'w' mode in 3.x
    my_dict = {}
    fieldnames = ['userId', 'testItems']
    w = csv.DictWriter(f,fieldnames=fieldnames)
    w.writeheader()
    for i in range(1, len(list)):
        my_dict['userId'] = list[i][0]
        my_dict['testItems'] = getRecommendations(urm, int(list[i][0]), 6)
        w.writerow(my_dict)
        print(my_dict)