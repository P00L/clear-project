import numpy as np
import csv

def apk(actual, predicted, k):
    """
    Computes the average precision at k.
    This function computes the average prescision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 0.0

    return score / min(len(actual), k)

def mapk(actual, predicted, k):
    """
    Computes the mean average precision at k.
    This function computes the mean average prescision at k between two lists
    of lists of items.
    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The mean average precision at k over the input lists
    """
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])

#open predicted item
#{user:[item]}
with open('test/cf_AdjCosine_skr6cosine_bias_noDenRanking_popularity_test.csv', 'r') as urm:
    reader = csv.reader(urm)
    predicted_dic = {}
    for row in reader:
        if row[0]!= 'userId':
            lista_str = str(row[1]).split(" ")[1:]
            lista_int = []
            for i in lista_str:
                lista_int.append(int(i))
            predicted_dic[int(row[0])]= lista_int

#open test item
#{user:[item]}
with open('test/test_split.csv', 'r') as urm:
    reader = csv.reader(urm)
    actual_dict = {}
    for row in reader:
        if row[0]!= 'userId':
                actual_dict.setdefault(int(row[0]),[]).append(int(row[1]))
predicted =[]
actual=[]
for user in predicted_dic:
    predicted.append(predicted_dic[user])
    actual.append(actual_dict[user])

print("reccomandation "+str(predicted))
print("real data "+str(actual))

print (mapk(actual,predicted,2))
