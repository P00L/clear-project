import csv

"""
R = mxn
avg = avg R media voto su tutta la matrice
R' = R - avg
bi = avg R' -----> sum over u of R'ui/ni +k ----> per ogni item sommo i rating che ha avuto e lo divido per il numero di rating
R'' = R' - bi = R - avg -bi
bu = avg R''
global effect = avg + bi + bu -----> per user u item i
vedi libro cremo (se non cel'hai te lo passo)
"""
#shrink
s=3

rating = [] #lista di tutti i rating presenti
urm_i ={}#{item:[lista di rating]}
urm_u = {}#{user:[lista di rating]}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    for row in reader:
        if row[0] != 'userId':
            rating.append(int(row[2]))
            urm_u.setdefault(int(row[0]), {})[int(row[1])] = int(row[2])
            urm_i.setdefault(int(row[1]), []).append(int(row[2]))

sum_r = 0
n = 0
for r in range(0,len(rating)):
    sum_r += rating[r]
    n += 1
avg = sum_r/n
print("avg = " + str(avg))

bi= {}
with open('resources/item_bias.csv', 'w', newline='') as f:
        my_dict = {}
        fieldnames = ['ItemId', 'bias']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for i in urm_i:
            sum_r = 0
            n = 0
            for r in urm_i[i]:
                sum_r += r - avg
                n += 1
            my_dict['ItemId'] = i
            bi[i] = sum_r/n+s
            my_dict['bias'] = sum_r/n+s
            w.writerow(my_dict)
print("item bias "+str(bi))

with open('resources/user_bias.csv', 'w', newline='') as f:
        my_dict = {}
        fieldnames = ['UserId', 'bias']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for u in urm_u:
            sum_r = 0
            n = 0
            for i in urm_u[u]:
                sum_r += urm_u[u][i] - avg -bi[i]
                n += 1
            my_dict['UserId'] = u
            my_dict['bias'] = sum_r/n+s
            w.writerow(my_dict)


