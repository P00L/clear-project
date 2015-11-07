__author__ = 'Federica'
from math import sqrt

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
    den = (squared_root(urm[user1])*squared_root(urm[user2]))+ skr
    return round(num/den, 3)

# similarity tra item per feautures
def similarity_item(dic, item1, item2):
    shared = 0
    if item1 not in dic or item2 not in dic:
        return 0
    for val in dic[item1]:
        if val in dic[item2]:
            shared += 1
    if shared == 0:
        return 0
    return round(shared / (len(dic[item1]) + len(dic[item2]) - shared), 3)


# returns the n=20 best match for each user
def top_n_match(dic, item1, skr, n=20):
    matched_items = []
    for item in dic:
        if item != item1:
            sim = similarity_cosine(dic, item1, skr)
            if sim != 0:
                matched_items.append((sim, item))
    matched_items.sort(reverse=True)
    return matched_items[0:n]





