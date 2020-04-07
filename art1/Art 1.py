#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
plt.ioff()


# In[2]:


sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10,6))


# In[3]:


shp_path = "./us_data/tl_2017_us_state.shp"
sf = shp.Reader(shp_path)


# In[4]:


print(len(sf.shapes()))


# In[5]:


def read_shapefile(sf):
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    
    return df


# In[6]:


df = read_shapefile(sf)
print(df.shape)


# In[7]:


df.head()


# In[8]:


def state_to_id(state):
#     print(state)
    return df[df.NAME == state].index.values[0]


# In[9]:


def plot_shape(id, s=None):
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
        
    plt.plot(x_lon, y_lat)
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    plt.xlim(shape_ex.bbox[0], shape_ex.bbox[2])
    return x0, y0


# In[10]:


def plot(title, ids, sf, x_lim=None, y_lim=None, figsize=(11,9), color='r'):
       
    plt.figure(figsize = figsize)
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(title, fontsize=16)
    
    no_print = [40, 31, 41, 35, 36, 49, 34]

    s_id = 0
    for shape in sf.shapeRecords():
        if(s_id not in no_print):
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            plt.plot(x, y, 'k')
        s_id = s_id + 1

    for id in ids:
        shape_ex = sf.shape(id)
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
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


# In[11]:


def remove_dups(data):
    da = []
    for d in data:
        if(d in da):
            pass
        else:
            da.append(d)
    return da


# In[12]:


from colour import Color
def colors_calc(data, c1, c2):
    rd = remove_dups(sorted(data))
    da = sorted(data)
#     print(da)
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
#     print(cs)
#     sns.palplot(list(cs.values()), 0.1 * len(rd))
    return cs


# In[13]:


def plot_states_data(sf, title, states, data, print_id=False, save_fig=True):
    colors = colors_calc(data, "green", "red")
    df = read_shapefile(sf)
    state_id = []
    for i in range(len(states)):
        if(not (df[df.NAME == states[i]].empty)):
            state_id.append(df[df.NAME == states[i]].index.values[0])
    plot_map_fill_multiple_ids_tone(sf, title, state_id, data, print_id, colors, x_lim = None, y_lim = None, figsize=(11,9), savefigb=save_fig)


# In[14]:


def plot_map_fill_multiple_ids_tone(sf, title, state, data, print_id, colors, x_lim = None, y_lim = None, figsize = (11,9), savefigb=True):
    plt.figure(figsize=figsize)
    fig, ax = plt.subplots(figsize = figsize)
    fig.suptitle(title, fontsize=16)
    
    no_print = [40, 31, 41, 35, 36, 49, 34]
    
    s_id = 0
    for shape in sf.shapeRecords():
#         print(s_id)
        if(s_id not in no_print):
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            ax.plot(x, y, 'k')
        s_id = s_id + 1
            
    
        for i in range(len(state)):
            id = state[i]
            cases = data[i]
            shape_ex = sf.shape(id)
            x_lon = np.zeros((len(shape_ex.points),1))
            y_lat = np.zeros((len(shape_ex.points),1))
            for ip in range(len(shape_ex.points)):
                x_lon[ip] = shape_ex.points[ip][0]
                y_lat[ip] = shape_ex.points[ip][1]
            ax.fill(x_lon,y_lat, colors[cases])
            if print_id != False:
                x0 = np.mean(x_lon)
                y0 = np.mean(y_lat)
                plt.text(x0, y0, str(cases), fontsize=10)
        if (x_lim != None) & (y_lim != None):     
            plt.xlim(x_lim)
            plt.ylim(y_lim)
        if savefigb:
            plt.savefig('./photos/' + title)
            plt.close(fig)
        


# In[15]:


# states = ['Oregon', 'Washington', 'Texas', "Idaho", "California", "New York"]
# data = [100000, 345, 1, 234, 235,2352]

# plot_states_data(sf, 'States', states, data, True, save_fig=True)


# In[16]:


import csv
import datetime


# In[17]:


def get_date(s):
    dto = datetime.datetime.strptime(s, '%Y-%m-%d')
    return dto


# In[18]:


def get_date_from_covid(ind, file='us-states-covid.csv'):
    i = 0
    with open(file) as cf:
        cr = csv.reader(cf, delimiter=',')
        for r in cr:
            if(i == 0):
                pass
            else:
                if i == ind:
                    return get_date(r[0])
            i += 1


# In[19]:


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
                
                # Next Day
                if date > prev_date:
                    i += 1
                    prev_date = date
                    dates.append([])
                    dates[i].append([r[1], r[3]])

                # Same day
                else:
                    dates[i].append([r[1], r[3]])
                lc += 1
        print(f'Procewssed {lc} lines')
        return dates


# In[20]:


cases = parse_covid('us-states-covid.csv')


# In[21]:


print(len(cases))


# In[22]:


def parse_date_entry(ca):
    states = []
    cases = []
    
    for c in ca:
        states.append(c[0])
        cases.append(int(c[1]))
    return states, cases


# In[23]:


def show_covid(i, cases):
    states, cases = parse_date_entry(cases[i])
    date = get_date_from_covid(i)
    # print(date, states, cases)
    plot_states_data(sf, str(date), states, cases, True, save_fig=True)


# In[24]:


# show_covid(6, cases)


# In[28]:


from tqdm import tqdm
for i in tqdm(range(len(cases))):
    show_covid(i, cases)


# In[ ]:




