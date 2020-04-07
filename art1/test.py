import csv
import datetime

def get_date(s):
    dto = datetime.datetime.strptime(s, '%Y-%m-%d')
    return dto

def get_date_from_covid(ind, file='test.csv'):
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
        print(f'Processed {lc} lines')
        return dates

cases = parse_covid('test.csv')

print(cases[len(cases)-1])
print(get_date_from_covid(len(cases)-1))
