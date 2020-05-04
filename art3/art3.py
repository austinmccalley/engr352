#!/usr/bin/env python
# coding: utf-8


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

sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10, 6))


shp_path = "./us_data/tl_2017_us_state.shp"
sf = shp.Reader(shp_path)

print(len(sf.shapes()))

def read_shapefile(sf):
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]

    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)

    return df



df = read_shapefile(sf)
print(df.shape)



def fip_to_state(fip):
    fip = str(fip)
    if len(fip) < 2:
        fip = '0' + fip

    print(fip, df[df.GEOID == fip].index)
    return df[df.GEOID == fip].index.values[0]

def state_to_id(state):
    return df[df.NAME == state].index.values[0]


# def plot_shape(id, s=None):
#     plt.figure()
#     ax = plt.axes()
#     ax.set_aspect('equal')
#     shape_ex = sf.shape(id)
#     x_lon = np.zeros((len(shape_ex.points), 1))
#     y_lat = np.zeros((len(shape_ex.points), 1))

#     for ip in range(len(shape_ex.points)):
#         x_lon[ip] = shape_ex.points[ip][0]
#         y_lat[ip] = shape_ex.points[ip][1]

#     plt.plot(x_lon, y_lat)
#     plt.xlim(shape_ex.bbox[0], shape_ex.bbox[2])
#     return x0, y0



def plot(title, ids, sf, x_lim=None, y_lim=None, figsize=(11, 9), color='r'):

    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=16)

    s_id = 0
    for shape in sf.shapeRecords():
        if(s_id not in no_print):
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            plt.plot(x, y, 'k')
        s_id = s_id + 1

    for id in ids:
        shape_ex = sf.shape(id)
        x_lon = np.zeros((len(shape_ex.points), 1))
        y_lat = np.zeros((len(shape_ex.points), 1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon, y_lat, color)

        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        plt.text(x0, y0, id, fontsize=10)

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)


def remove_dups(data):
    da = []
    for d in data:
        if(d in da):
            pass
        else:
            da.append(d)
    return da



def lists_to_listi(ls):
    li = []
    for e in ls:
        li.append(int(e))
    return li



def colors_calc(data, c1, c2):
    # vals = lists_to_listi(data.values())
    vals = data.values()
    rd = remove_dups(sorted(vals))
    da = sorted(vals)
    cs = {}
    c = Color(c1)
    colors = list(c.range_to(Color(c2), len(rd)))

    prev = 0
    dups = 0
    for i in range(len(da)):
        if i == 0:
            cs[da[i]] = colors[i].hex
        else:
            if da[prev] != da[i]:
                cs[da[i]] = colors[(i - dups)].hex
            else:
                dups += 1
        prev = i

    cs[0] = "#ffffff"
#     Un-comment below to see a graphical representation of the gradient colors used.
#     sns.palplot(list(cs.values()), 0.1 * len(rd))
    return cs


def sid_to_s(sid):
    n = df['NAME']
    return n[sid]



def plot_states_data(sf, title, states, data, print_id=False, save_fig=True):
    colors = colors_calc(data, "green", "red")
    df = read_shapefile(sf)
    state_id = []

    no_print = ["Hawaii", "Guam", "Puerto Rico", "Alaska",
                "Northern Mariana Islands", "Virgin Islands", "American Samoa"]
    for i in range(len(states)):
        if(not (df[df.NAME == states[i]].empty) and states[i] not in no_print):
            state_id.append(df[df.NAME == states[i]].index.values[0])
    plot_map_fill_multiple_ids_tone(
        sf, title, state_id, data, print_id, colors, x_lim=None, y_lim=None, savefigb=save_fig)


def plot_map_fill_multiple_ids_tone(sf, title, state, data, print_id, colors, x_lim=None, y_lim=None, figsize=(11, 9), savefigb=True):
    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize=figsize, dpi=75)
    fig.suptitle(str(title)[:10] + ' State Population Infected', fontsize=16)
    ax.set_aspect('equal')

    sip = []

    for i in range(len(state)):
        id = state[i]
        state_name = sid_to_s(id)
        cases = data[state_name]

#         print(state_name, id)

        shape_ex = sf.shape(id)
        x_lon = np.zeros((len(shape_ex.points), 1))
        y_lat = np.zeros((len(shape_ex.points), 1))

        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]

        ax.fill(x_lon, y_lat, colors[cases])

        if print_id != False:
            x0 = np.mean(x_lon)
            y0 = np.mean(y_lat)
            ''' str(cases)'''
            plt.text(x0, y0,  str(cases), fontsize=7,
                     va='center', ha='center')

    no_print = [40, 31, 41, 35, 36, 49, 34]
    s_id = 0
    for shape in sf.shapeRecords():
        if(s_id not in no_print):

            sn = sid_to_s(s_id)
            ss = None

            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            if ss is not None:
                if ss == title or title > ss:
                    #                     print(sn, "SIP")
                    ax.plot(x, y, c='#0000ff', linewidth=2)
                else:
                    ax.plot(x, y, 'k')
            else:
                if title == get_date('2020-04-05'):
                    ax.plot(x, y, c='#ff0000')
                else:
                    ax.plot(x, y, c='k')

        s_id = s_id + 1

        if (x_lim != None) & (y_lim != None):
            plt.xlim(x_lim)
            plt.ylim(y_lim)
        if savefigb:
            fig.savefig('./photos/map/' + str(title)[:10])
            plt.close(fig)


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
        print(f'Processed {lc} lines with a total of {len(dates)} different days' )
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

pop = parse_pop('population.csv')

def get_pop(state):
    if (state in pop.keys()):
        return pop[state]
    else:
        return 1
    
def create_dict(cases):
    ca = {}
    for c in cases:
        state = c[0]
        cases = c[1]
        pop = get_pop(state)
        if(cases != "0"):
            diff = round(float(cases) / float(pop) * 100.0, 7)
            diff = str(diff) + "%"
        else:
            diff = "Null"
        ca[state] = diff
    return ca

def parse_date_entry(ca):
    states = []
    cases = []

    for c in ca:
        states.append(c[0])
        cases.append(int(c[1]))
    return states, cases


def show_covid(i, _cases):
    states, _ = parse_date_entry(_cases[i])
    cases = create_dict(_cases[i])
    date = get_date_from_covid(i)
    print(cases, date)

    plot_states_data(sf, date, states, cases, True, save_fig=True)






for i in tqdm(range(len(cases))):
    show_covid(i, cases)

