from math import sqrt
__author__ = 'Federica'


def similarity_distance(urm,user_1,user_2):
    """
    * WARNING:
        * DUNNO IF SOMEONE WANNA USE THIS... IT'S TOTALLY CRAP IMHO, BUT NOT TO BE DEPRECATED
    Parameters
    ----------
    urm
    user_1
    user_2

    Returns
    -------
    NOTHING USEFUL
    """
    # Get the list of shared_items
    si = {}
    for item in urm[user_1]:
        if item in urm[user_2]:
            si[item] = 1
    # if they have no ratings in common, return 0
    if len(si) == 0:
        return 0
    # Add up the squares of all the differences
    sum_of_squares=sum([pow(urm[user_1][item]-urm[user_2][item], 2) for item in urm[user_1] if item in urm[user_2]])
    return 1/(1+sum_of_squares)


def similarity_pearson(urm, user_1, user_2, skr=0):
    """
    Compute the Pearson similarity (google to know what is it): it works well only with users

    WARNING:
        It seems this kind of similarity doesn't work very well with our data set, so I suggest not to use it

    :param urm: user rating matrix
    :param user_1: user 1
    :param user_2: user 2
    :param skr: shrink term (DEFAULT 0)
    :return: Pearson similarity between two users
    """
    # Get the list of mutually rated items
    si = {}
    for item in urm[user_1]:
        if item in urm[user_2]: si[item]=1

    # Find the number of elements
    n = len(si)
    # if they are no ratings in common, return 0
    if n == 0:
        return 0
    # Add up all the preferences
    sum1 = sum([urm[user_1][it] for it in si])
    sum2 = sum([urm[user_2][it] for it in si])
    # Sum up the squares
    sum1_sq = sum([pow(urm[user_1][it], 2) for it in si])
    sum2_sq = sum([pow(urm[user_2][it], 2) for it in si])
    # Sum up the products
    p_sum = sum([urm[user_1][it]*urm[user_2][it] for it in si])
    # Calculate Pearson score
    num = p_sum-(sum1*sum2/n)
    den = (sqrt((sum1_sq-pow(sum1, 2)/n)*(sum2_sq-pow(sum2, 2)/n)) + skr)
    if den == 0:
        return 0

    r = round(num/den, 3)
    return r


def squared_root(x):
    """
    This function return the sum of the squared roots of the value

    :param x: dict of values
    :return: a float that is the sum of the squared roots
    """
    return round(sqrt((sum([x[val] * x[val] for val in x]))), 3)


def cosine_sim(dic, item1, item2, skr=0):
    """
    Compute the cosine similarity between two items

    :param dic: the dictionary where i find the two items
    :param item1: first item
    :param item2: second item
    :param skr: shrink term to be added at denominator
    :return: float that represents the cosine similarity of the two ==> 0 means no similarity
    """
    shared_1 = {}
    shared_2 = {}
    for val in dic[item1]:
        if val in dic[item2]:
            shared_1[val] = dic[item1][val]
            shared_2[val] = dic[item2][val]
    if len(shared_1) == 0:
        return 0
    num = sum([shared_1[val]*shared_2[val] for val in shared_1])
    den = squared_root(dic[item1])*squared_root(dic[item2])
    return round(num/(den + skr), 3)


def item_sim(dic, item1, item2, skr=0):
    """
    Compute an item similarity when the attribute are binary

    This kind of similarity is computed as:
        *num of shared attr / (num of attr of item1 + num of attr of item2 - num of shared attr)

    :param dic: the dictionary where i find the two items
    :param item1: first item
    :param item2: second item
    :param skr: shrink term
    :return: float that represents the item similarity
    """
    shared = 0
    if item1 not in dic or item2 not in dic:
        return 0
    for val in dic[item1]:
        if val in dic[item2]:
            shared += 1
    if shared == 0:
        return 0
    return round(shared / (len(dic[item1]) + len(dic[item2]) - shared + skr), 3)


def top_n_match(dic, item, skr=0, n=20, similarity=cosine_sim):
    """
    * TODO:
        # try to change the parameters of :param skr :param n to see if the score change in a significant way

    Implementation of the k-NN (k Nearest Neighbor) measure

    * WARNING:
        it seems to work a lot better with cosine similarity

    :param dic: the dict containing the item
    :param item: the item i want the list
    :param skr: the shrink term to be applied (DEFAULT is 0)
    :param n: the number of neighbor I want (DEFAULT is 20)
    :param similarity: kind of similarity used (DEFAULT is cosine similarity)
    :return: a dict of at least n entries formed by {userId: similarity)
    """
    matched_items = []
    for other_item in dic:
        if other_item != item:
            sim = similarity(dic, item, other_item, skr)
            if sim != 0:
                matched_items.append((sim, other_item))
                matched_items.sort(reverse=True)
                matched_items = matched_items[0:n]
    if len(matched_items) < 5:
        for item in dic:
            if item != item:
                sim = cosine_sim(dic, item, other_item, skr)
                if sim != 0:
                    matched_items.append((sim, other_item))
                    matched_items.sort(reverse=True)
                    matched_items = matched_items[0:n]
    nearest = {}
    for (sim, other_item) in matched_items:
        nearest[other_item] = sim
    return nearest





