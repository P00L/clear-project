# Daniel Alabi and Cody Wang
# ======================================
# SvdMatrix:
# generates matrices U and V such that
# U * V^T closely approximates
# the original matrix (in this case, the utility
# matrix M)
# self.U[uid], self.V[mid]
#numero user for us = 15374
#numero item for us = 37142
#ricorda gli elementi nella matrice U e V sono scalati di -1 rispetto ai nostri valori
# =======================================
import math
import csv
import random
import datetime


"""
Rating class. 
Store every rating associated with a particular
userid and movieid.
================Optimization======================
"""
class Rating:
    def __init__(self, userid, movieid, rating):
        # to accomodate zero-indexing for matrices
        self.uid = userid-1 
        self.mid = movieid-1

        self.rat = rating


class SvdMatrix:
    """
    trainfile -> name of file to train data against
    nusers -> number of users in dataset
    nmovies -> number of movies in dataset
    r -> rank of approximation (for U and V)
    lrate -> learning rate
    regularizer -> regularizer
    typefile -> 0 if for smaller MovieLens dataset
                1 if for medium or larger MovieLens dataset
    """
    def __init__(self, nusers, nmovies, r=115, lrate=0.11, regularizer=0.025):
        self.trainrats = []#la nostra urm sotto forma di lista di oggetti Rating
        self.testrats = []
                
        self.nusers = nusers
        self.nmovies = nmovies

        self.readinratings(self.trainrats)

        # get average rating
        self.avg = self.averagerating()
        # set initial values in U, V using square root
        # of average/rank
        initval = math.sqrt(self.avg/r)
        # U matrix
        self.U = [[initval]*r for i in range(nusers)]
        # V matrix -- easier to store and compute than V^T
        self.V = [[initval]*r for i in range(nmovies)]

        self.r = r #le nostre k feature
        self.lrate = lrate
        self.regularizer = regularizer
        self.minimprov = 0.0008
        self.maxepochs = 10


    """
    Returns the dot product of v1 and v2
    """
    def dotproduct(self, v1, v2):
        return sum([v1[i]*v2[i] for i in range(len(v1))])

    """
    Returns the estimated rating corresponding to userid for movieid
    Ensures returns rating is in range [1,10]
    p = predicted rating(dot prduct) + avg + user bias + item bias
    """
    def calcrating(self, uid, mid):
        p = self.dotproduct(self.U[uid], self.V[mid]) + self.avg + user_bias[uid] + item_bias[mid]
        if p > 10:
            p = 10
        elif p < 1:
            p = 1
        return p

    """
    Returns the average rating of the entire dataset
    """
    def averagerating(self):
        avg = 0
        n = 0
        for i in range(len(self.trainrats)):
            avg += self.trainrats[i].rat
            n += 1
        return float(avg/n)

    """
    Predicts the estimated rating for user with id i
    for movie with id j
    """
    def predict(self, i, j):
        return self.calcrating(i, j)

    """
    Trains the kth column in U and the kth row in
    V^T
    See docs for more details.
    """
    def train(self, k):
        sse = 0.0
        n = 0
        #scandisce tutti i rating dell'urm
        for i in range(len(self.trainrats)):
            # get current rating
            crating = self.trainrats[i]
            #vedi predict per la predizione
            err = crating.rat - self.predict(crating.uid, crating.mid)
            #spero sia giusto vedi SVD libro di recco consiglaito da cremo(se non cel'hai te lo passo)
            #non sono sicuro sulle norme dei bias in teoria la norma e la somma degli elementi al quadrato sotto radice, ma siccome da noi
            #vuola la norma al quadrato ho lasciato solo la somma degli elementi (forse manca al quadrato)
            sse += err**2 + self.regularizer * (user_bias[crating.uid]**2 + item_bias[crating.mid]**2 + sum(i*i for i in self.U[crating.uid]) +sum(i*i for i in self.V[crating.mid]))
            n += 1

            #store temporary old value
            uTemp = self.U[crating.uid][k]
            vTemp = self.V[crating.mid][k]
            user_bias_temp = user_bias[crating.uid]
            item_bias_temp = item_bias[crating.mid]

            self.U[crating.uid][k] += self.lrate * (err*vTemp - self.regularizer*uTemp)
            self.V[crating.mid][k] += self.lrate * (err*uTemp - self.regularizer*vTemp)
            user_bias[crating.uid] += self.lrate * (err - self.regularizer * user_bias_temp)
            item_bias[crating.mid] += self.lrate * (err - self.regularizer * item_bias_temp)

            #idea per fare il train di alcuni zero random(assunzione se manca e zero)
            """
            n_zero_trained = 0
            for x in range(0,1000):
                random_user = random.randint(0,15373)
                random_item = random.randint(0,37142)
                if random_item not in urm[random_user]:
                    n_zero_trained += 1
                    err = -self.predict(random_user, random_item)
                    sse += err**2 + self.regularizer * (user_bias[crating.uid]**2 + item_bias[crating.mid]**2 + sum(self.U[crating.uid]) +sum(self.V[crating.mid]))
                    n += 1
                   #store temporary old value
                    uTemp = self.U[crating.uid][k]
                    vTemp = self.V[crating.mid][k]
                    user_bias_temp = user_bias[crating.uid]
                    item_bias_temp = item_bias[crating.mid]

                    self.U[crating.uid][k] += self.lrate * (err*vTemp - self.regularizer*uTemp)
                    self.V[crating.mid][k] += self.lrate * (err*uTemp - self.regularizer*vTemp)
                    user_bias[crating.uid] += self.lrate * (err - self.regularizer * user_bias_temp)
                    item_bias[crating.mid] += self.lrate * (err - self.regularizer * item_bias_temp)
            print("random zero trained = " + str(n_zero_trained))
            """
        return math.sqrt(sse/n)

    """
    Trains the entire U matrix and the entire V (and V^T) matrix
    """
    def trainratings(self):
        # stub -- initial train error
        oldtrainerr = 1000000.0
       #scndisce tutte le k feature
        for k in range(self.r):
            print ("k="+ str(k))
            for epoch in range(self.maxepochs):
                trainerr = self.train(k)
                
                # check if train error is still changing
                if abs(oldtrainerr-trainerr) < self.minimprov:
                    break
                oldtrainerr = trainerr
                print ("epoch="+ str(epoch)+ "; trainerr="+ str(trainerr))
                
    """
    Calculates the RMSE using between arr
    and the estimated values in (U * V^T)
    """
    def calcrmse(self, arr):
        nusers = self.nusers
        nmovies = self.nmovies
        sse = 0.0
        total = 0
        for i in range(len(arr)):
            crating = arr[i]
            sse += (crating.rat - self.calcrating(crating.uid, crating.mid))**2
            total += 1
        return math.sqrt(sse/total)

    """
    Read in the ratings from train and put in arr
    """
    def readinratings(self,arr):
        #arr in realta e train rats
        with open('resources/train.csv', 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0]!= 'userId':
                    userid, movieid, rating = int(row[0]), int(row[1]), float(row[2])
                    arr.append(Rating(userid, movieid, rating))

        arr = sorted(arr, key=lambda rating: (rating.uid, rating.mid))
        return len(arr)

    """
    Returns the estimated rating corresponding to userid for movieid
    DON'T RETURN VALUE BEETWEEEN 1 AND 10 FOR BETTER ORDERING CREDO,SPERO
    """
    def predict_rate(self,uid,mid):
        p = self.avg + user_bias[uid] + item_bias[mid] + self.dotproduct(self.U[uid], self.V[mid])
        return p

with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    user_test_list = list(reader)

#item bias gia riscalato di -1 per matchare gli indici
item_bias = {}
with open('resources/item_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'ItemId':
            item_bias[int(row[0])-1] = float(row[1])

#item bias gia riscalato di -1 per matchare gli indici
user_bias = {}
with open('resources/user_bias.csv', 'rt') as f:
    reader = csv.reader(f)
    i = 1
    for row in reader:
        if row[0] != 'UserId':
            user_bias[int(row[0])-1] = float(row[1])

#riempio user_bias e item_bias per fillare i valori mancanti
for i in range(0,15373):
    if i not in user_bias:
        user_bias[i] = float(0)

for i in range(0,37142):
    if i not in item_bias:
        item_bias[i] = float(0)

urm = {}
# urm --> {user:[item]}
#serve per controllare di non raccomandare film gia visti
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]),[]).append(int(row[1]))

if __name__ == "__main__":
    init = datetime.datetime.now()
    svd = SvdMatrix(15374, 37142)#inizializza la classe svdMttrix
    svd.trainratings()
    print ("rmsetrain: "+ str(svd.calcrmse(svd.trainrats)))
    print ("time: "+ str(datetime.datetime.now()-init))
    with open('submission/SVD_globalEffect_maxepochs10_minimprov0,0008_regularizer0,03_lrate0,2_r115.csv', 'w', newline='') as f:
        my_dict = {}
        rankings = []
        fieldnames = ['userId', 'testItems']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for u in range(1,len(user_test_list)):
            rankings = []
            for i in range(1,37143):
                if i not in urm[int(user_test_list[u][0])]:
                    #-1 perche accesso posizionale nella lista scalato di 1 (vedi classe Ratings)
                    rankings.append((svd.predict_rate(int(user_test_list[u][0])-1,i-1),i))
            rankings.sort()
            rankings.reverse()
            rankings_cut = rankings[0:5]
            result = ""
            for i in range(len(rankings_cut)):
                result = result + " " + str(rankings_cut[i][1])
            my_dict['userId'] = user_test_list[u][0]
            my_dict['testItems'] = result
            w.writerow(my_dict)
            print(str(my_dict['userId']) + "," + str(my_dict['testItems']))
        print ("time: "+ str(datetime.datetime.now()-init))