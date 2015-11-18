# Daniel Alabi and Cody Wang
# ======================================
# SvdMatrix:
# generates matrices U and V such that
# U * V^T closely approximates
# the original matrix (in this case, the utility
# matrix M)
#
#1) costruttore  SvdMatrix class
#2) readtrainsmaller
#3) readinratings
#4) class Rating un sacco di volte
#5) averagerating
#6) trainratings
#   7)for su k
#   8)train una volta per k
#       9)predict un po di voolte per k
#       10)calcrating un po di voolte per k
#       11)dotproduct un po di voolte per k
#
#
# self.U[uid], self.V[mid]
#numero user for us = 15374
#numero item for us = 37142
# =======================================
import math
import csv
import random
import time


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
    def __init__(self, trainfile, nusers, nmovies, r=30, lrate=0.035, regularizer=0.01, typefile=0):
        self.trainrats = []#la nostra urm sotto forma di lista di oggetti Rating
        self.testrats = []
                
        self.nusers = nusers
        self.nmovies = nmovies

        if typefile == 0:
            self.readtrainsmaller(trainfile)
        elif typefile == 1:
            self.readtrainlarger(trainfile)

        # get average rating
        avg = self.averagerating()
        # set initial values in U, V using square root
        # of average/rank
        initval = math.sqrt(avg/r)
        
        # U matrix
        self.U = [[initval]*r for i in range(nusers)]
        # V matrix -- easier to store and compute than V^T
        self.V = [[initval]*r for i in range(nmovies)]

        self.r = r #le nostre k feature
        self.lrate = lrate
        self.regularizer = regularizer
        self.minimprov = 0.001
        self.maxepochs = 30            

    """
    Returns the dot product of v1 and v2
    """
    def dotproduct(self, v1, v2):
        return sum([v1[i]*v2[i] for i in range(len(v1))])

    """
    Returns the estimated rating corresponding to userid for movieid
    Ensures returns rating is in range [1,10]
    """
    def calcrating(self, uid, mid):
        p = self.dotproduct(self.U[uid], self.V[mid])
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
            err = crating.rat - self.predict(crating.uid, crating.mid)
            sse += err**2
            n += 1

            uTemp = self.U[crating.uid][k]
            vTemp = self.V[crating.mid][k]

            self.U[crating.uid][k] += self.lrate * (err*vTemp - self.regularizer*uTemp)
            self.V[crating.mid][k] += self.lrate * (err*uTemp - self.regularizer*vTemp)
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
    Read in the ratings from fname and put in arr
    Use splitter as delimiter in fname
    """
    def readinratings(self, fname, arr, splitter="\t"):
        """
        f = open(fname)

        for line in f:
            newline = [int(each) for each in line.split(splitter)]
            userid, movieid, rating = newline[0], newline[1], newline[2]
            arr.append(Rating(userid, movieid, rating))
        """
        #arr in realta e train rats
        with open('resources/train.csv', 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0]!= 'userId':
                    userid, movieid, rating = int(row[0]), int(row[1]), int(row[2])
                    arr.append(Rating(userid, movieid, rating))


        arr = sorted(arr, key=lambda rating: (rating.uid, rating.mid))
        return len(arr)
        
    """
    Read in the smaller train dataset
    """
    def readtrainsmaller(self, fname):
        return self.readinratings(fname, self.trainrats, splitter="\t")
        
    """
    Read in the large train dataset
    """
    def readtrainlarger(self, fname):
        return self.readinratings(fname, self.trainrats, splitter="::")
        
    """
    Read in the smaller test dataset
    """
    def readtestsmaller(self, fname):
        return self.readinratings(fname, self.testrats, splitter="\t")
                
    """
    Read in the larger test dataset
    """
    def readtestlarger(self, fname):
        return self.readinratings(fname, self.testrats, splitter="::")



with open('resources/test.csv', 'rt') as f:
    reader = csv.reader(f)
    user_test_list = list(reader)

urm = {}
# urm --> {user:[item]}
#serve per controllare di non raccomandare film gia visti
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    for row in reader:
        if row[0] != 'userId':
            urm.setdefault(int(row[0]),[]).append(int(row[1]))

if __name__ == "__main__":
    #========= test SvdMatrix class on smallest MovieLENS dataset =========
    init = time.time()
    #Don't worry about a thing,Cause every little thing gonna be all right........
    #no dai a parte gli scherzi non guardate che e sbagliato ua.base tanto poi non viene considerato xD
    svd = SvdMatrix("ua.base", 15374, 37142)#inizializza la classe svdMttrix
    svd.trainratings()
    print ("rmsetrain: "+ str(svd.calcrmse(svd.trainrats)))
    print ("time: "+ str(time.time()-init))
    print("USER 1 ITEM 2738 RATING 1------>stima = "+str(svd.dotproduct(svd.U[2737],svd.V[0])))
    with open('submission/matrix_factorization_svd.csv', 'w', newline='') as f:
        my_dict = {}
        rankings = []
        fieldnames = ['userId', 'testItems']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for u in range(1,len(user_test_list)):
            rankings = []
            for i in range(0,37142):
                if i not in urm[int(user_test_list[u][0])]:
                    rankings.append((svd.dotproduct(svd.U[int(user_test_list[u][0])-1],svd.V[i-1]),i))
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
        print ("time: "+ str(time.time()-init))