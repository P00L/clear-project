import csv

urm_i={}#{item:[lista di rating]}
urm_u = {}#{user:[lista di rating]}
with open('resources/train.csv', 'r') as urm_raw:
    reader = csv.reader(urm_raw)
    for row in reader:
        if row[0] != 'userId':
            urm_u.setdefault(int(row[0]), {})[int(row[1])] = int(row[2])
            urm_i.setdefault(int(row[1]), []).append(int(row[2]))


with open('resources/user_avg.csv', 'w', newline='') as f:
        my_dict = {}
        fieldnames = ['UserId', 'avg']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for u in urm_u:
            sum_r = 0
            n = 0
            for i in urm_u[u]:
                sum_r += urm_u[u][i]
                n += 1
            my_dict['UserId'] = u
            my_dict['avg'] = round(sum_r/n,5)
            w.writerow(my_dict)

with open('resources/item_avg.csv', 'w', newline='') as f:
        my_dict = {}
        fieldnames = ['ItemId', 'avg']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for i in urm_i:
            sum_r = 0
            n = 0
            for r in urm_i[i]:
                sum_r += r
                n += 1
            my_dict['ItemId'] = i
            my_dict['avg'] = round(sum_r/n,5)
            w.writerow(my_dict)