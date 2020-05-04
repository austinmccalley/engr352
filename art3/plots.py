from tqdm import tqdm
import time
import datetime
import csv
from colour import Color
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import math
import itertools

def get_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def get_date_from_covid(ind, file='us-states-covid.csv'):
    i = 0
    pd = get_date('2019-12-30')
    with open(file) as cf:
        cr = csv.reader(cf, delimiter=',')
        for r in cr:
            if r[0] == 'date':
                pass
            else:
                date = get_date(r[0])

                #  Next Day
                if date > pd:
                    if i == ind:
                        return date
                    i += 1
                    pd = date


def parse_covid(file):
    dates = []
    with open(file) as cf:
        cols = []
        cr = csv.reader(cf, delimiter=',')

        lc = 0
        prev_date = get_date('2019-12-30')
        i = -1

        for r in cr:
            if lc == 0:
                cols = r
                print(f'{cols}')
                lc += 1
            else:
                date = get_date(r[0])
                # print(prev_date, date)

                #  Next Day
                if date > prev_date:
                    # print('New day')
                    i += 1
                    prev_date = date
                    dates.append([])
                    dates[i].append([r[1], r[3]])

                # Same day
                elif date == prev_date:
                    dates[i].append([r[1], r[3]])
                else:
                    print("ERROR")
                    exit(0)

                lc += 1
        print(
            f'Processed {lc} lines with a total of {len(dates)} different days')
        return dates


cases = parse_covid('us-states-covid.csv')


def parse_pop(file):
    s_pop = {}
    with open(file, 'r') as cf:
        cols = []
        cr = csv.reader(cf, delimiter=',')
        lc = 0
        for r in cr:
            if lc == 0:
                cols = r
                lc += 1
            else:
                s = r[0]
                pop = r[1]
                s_pop[s] = pop
                lc += 1
    return s_pop


def create_dict_per_date(cases):
    ca = {}
    i = 0
    for cl in cases:
        date = str(get_date_from_covid(i))
        for c in cl:
            state = c[0]
            cases = c[1]
            if date not in ca.keys():
                ca[date] = [{state: cases}]
            else:
                ca[date].append({state: cases})
        i += 1
    return ca

def create_dict_per_state(dd):
    ca = {}
    for obj in dd.keys():
        for d in dd[obj]:
            state = list(d.keys())[0]
            if state not in ca.keys():
                ca[state] = [d[state]]
            else:
                ca[state].append(d[state])
    return ca
        
    
def get_delta_per_state(ds):
    ca = {}
    for s in ds.keys():
        cases = ds[s]
        
        for i in range(len(cases)):
            if i != 0:
                prev = i - 1
                diff = (float(cases[i]) - float(cases[prev]))
                if s not in ca.keys():
                    ca[s] = [diff]
                else:
                    ca[s].append(diff)
    return ca


def get_first_day(st):
    for d in dd:
        for sts in dd[d]:
            if st in sts.keys():
                return d
            
    return 'NULL'

def graph_state(st, delta_s):


    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    day = get_first_day(st)
    plt.title(st + ", Δ cases starting " + day[:10])
    plt.ylabel('Δ cases per day')
    plt.xlabel('Days since first report of cases')

    Y = delta_s
    X = list(range(len(delta_s)))
    plt.plot(X, Y, label="current data")
    
    Z = np.poly1d(np.polyfit(X, Y, 6))


    for i in range(1, math.floor(len(delta_s) * 0.15)):
        prev = X[len(X) - 1]
        X.append(prev + 1)



    
    plt.plot(X, Z(X), '-', label="future prediction")
    plt.legend(loc='upper left')
    plt.grid(True)
    
    fig.savefig('./photos/plots/' + str(st + " " + day[:10]))
    plt.close(fig)
    
    
cases = parse_covid('us-states-covid.csv')

dd = create_dict_per_date(cases)


ds = create_dict_per_state(dd)

delta_s = get_delta_per_state(ds)

for s in tqdm(delta_s.keys()):
    graph_state(s, delta_s[s])

