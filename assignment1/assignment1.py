from __future__ import division
import csv
import operator
import tabulate
import matplotlib.pyplot as plt
from collections import defaultdict

def aggregator(reader):
    aggregated = defaultdict(int)

    for row in reader:
            aggregated[row["Organization Name"]] += int(row["Views per Month"])
    return aggregated

def sorter(aggregated):
    sorted_dict = sorted(aggregated.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_dict

def top(sorted_dict):
    x = 0
    top = []
    while x < 10:
       top.append(sorted_dict[x])
       x+=1
    return top

def drawTable(top):

    print tabulate.tabulate(top, headers=["Organization","Views per Month"])

    return


def drawChart(x_val, y_val, xticks):
    plt.bar(x_val,y_val,10)
    plt.xticks(x_val,xticks,fontsize=10, rotation='vertical' )
    plt.xlabel('Organization Name')
    plt.ylabel('Views per Month')
    plt.title('Top 10 Visitors')
    plt.grid(True)
    plt.show()


def main():


    #f = open(sys.argv[1], 'rU')
    f = open('data.csv', 'rU')
    try:
        reader = csv.DictReader(f,skipinitialspace=True)
        aggregated = aggregator(reader)
        sorted_dict = sorter(aggregated)
        top_ten = top(sorted_dict)



        y_val = [i[1] for i in top_ten]
        x_val = [20,40,60,80,100,120,140,160,180,200]
        xticks = [i[0] for i in top_ten]

        drawTable(top_ten)
        drawChart(x_val,y_val,xticks)


    finally:
        f.close()

main()