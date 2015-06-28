from __future__ import division
from datetime import datetime
from datetime import timedelta
import tabulate
import operator
import matplotlib.pyplot as plt
from collections import defaultdict


def aggregateAvg(array):

    dates = []
    activities = []
    d = timedelta(days=14).total_seconds()


    for row in range(2,len(array)):
        t1 = datetime.strptime(array[row][1], "%Y-%m-%d %H:%M:%S")
        t2 = datetime.strptime(array[row][0], "%Y-%m-%d %H:%M:%S")

        difference = t1 - t2


        dates.append(difference.total_seconds())
        activities.append(array[row][2])

    tups = zip(activities,dates)

    dict = defaultdict(float)
    for (act, dat) in tups:
        dict[act] +=(dat)/d


    return dict

def aggregateDates(array):

    dates = []
    activities = []


    for row in range(2,len(array)):
        t1 = datetime.strptime(array[row][1], "%Y-%m-%d %H:%M:%S")
        t2 = datetime.strptime(array[row][0], "%Y-%m-%d %H:%M:%S")

        difference = t1 - t2


        dates.append(difference)
        activities.append(array[row][2])

    tups = zip(activities,dates)

    dict = defaultdict(timedelta)
    for (act, dat) in tups:
        dict[act] += dat


    return dict


def activityDuration(array):

    totals = []
    x = 0
    for row in range(2,len(array)):
        t1 = datetime.strptime(array[row][1], "%Y-%m-%d %H:%M:%S")
        t2 = datetime.strptime(array[row][0], "%Y-%m-%d %H:%M:%S")

        difference = t1 - t2

        totals.append([])
        totals[x].append(difference)
        totals[x].append(array[row][2])

        x+=1

    return totals

def printCumTotals(dict):

    table = []
    table.append(dict)

    print("\nCumulative time spent on activities over 14 days\n\n")
    print tabulate.tabulate(table, headers="keys")

def printAverages(dict):

    table = []
    table.append(dict)

    print("\nPercent of time spent on activities over 14 days")
    print tabulate.tabulate(table, headers="keys")



def printActivityTotals(array):


    print ("Time Spent Per Activity Instance\n\n")
    print tabulate.tabulate(array, headers=["Time Spent","Activity"])




def read_file():
    source = []
    with open('data.csv') as data:
        for line in data:
            source.append(line.strip().split('\t\t'))

    return source

def drawChart(dict):

    values  = sorted(dict.items(), key=operator.itemgetter(1))


    y_val = [i[1] for i in values]
    xticks = [i[0] for i in values]

    x_val = [20,40,60,80,100,120,140,160,180]
    plt.bar(x_val,y_val,10)
    plt.xticks(x_val,xticks,fontsize=10, rotation='vertical' )
    plt.xlabel('Activity')
    plt.ylabel('Percent of time Spent')
    plt.title('Percent of Time Spent on Activities')
    plt.grid(True)
    plt.show()

def main():

    l = []
    #f = open(sys.argv[1], 'rU')
    with open('data.csv') as data:
        for line in data:
            l.append(line.strip().split('\t\t'))

    totals = activityDuration(l)
    printActivityTotals(totals)

    dict = aggregateDates(l)

    printCumTotals(dict)

    avgdict= aggregateAvg(l)
    printAverages(avgdict)

    drawChart(avgdict)


main()