import tabulate
import operator
from collections import defaultdict


#This function is used to strip tags from the rdf files so that we can get at the raw data.
#It takes a string, and the opening and closing tags, returning the string in between the tags.
def stripTags( s, otag, ctag ):
    
    first = s.index( otag ) + len( otag )
    last = s.index( ctag, first )
    
    return s[first:last]

#This function grabs the ethnicity for the deaths reported in NYC.
# It returns an array containing the records.

def getEthnicity():
    records = []
    with open("nycdeaths.rdf", 'r') as file:
        for i in file:
            if "<ds:ethnicity>" in i:
                x = stripTags(i,"<ds:ethnicity>","</ds:ethnicity>")
                records.append(x)

    return records

#This retrieves the cause of death from the rdf file.
#It returns an array containing the records.

def getDeathCause():
    records = []
    with open("nycdeaths.rdf", 'r') as file:
        for i in file:
            if "<ds:cause_of_death>" in i:
                x = stripTags(i,"<ds:cause_of_death>","</ds:cause_of_death>")
                records.append(x)
    return records

#This retrieves the death counts per each reported cause of death
#It returns an array containing the records

def getDeathCount():
    records = []
    with open("nycdeaths.rdf", 'r') as file:
        for i in file:
            if "<ds:count>" in i:
                x = stripTags(i,"<ds:count>","</ds:count>")
                records.append(x)
    return records

#This function retrieves the demographic data from the 2010 census data so that we can correlate with the deaths.
#It returns an array of the the records

def getDemographics():
    records = []
    with open("nycdemographics.rdf", 'r') as file:
        for i in file:
            if "<ds:count_hispanic_latino>" in i:
                x = stripTags(i,"<ds:count_hispanic_latino>","</ds:count_hispanic_latino>")
                records.append(x)

    return records


#This function is used to retrieve only the deaths that reported a victim of HISPANIC ethnicity.
#It returns an array of the records.

def getHispDeaths(arr):

    records = []
    counter = 0

    while counter < len(arr):
        if arr[counter][1] == "HISPANIC":
            records.append(arr[counter])
        counter +=1

    return records

#This gets the name of the jurisdiction in which the demographics were collected.
#It returns an array of the records.
def getJurisdiction():
    records = []
    with open("nycdemographics.rdf", 'r') as file:
        for i in file:
            if "<ds:jurisdiction_name>" in i:
                x = stripTags(i,"<ds:jurisdiction_name>","</ds:jurisdiction_name>")
                records.append(x)

    return records

#This builds a table that displays the raw data that we collected for nycdeaths.rdf and prints it to the screen.

def buildTable1(jname, nhisp):

    i = 0
    counter = 0
    arr = []
    while i < len(jname):
        arr.append([])
        arr[counter].append(jname[i])
        arr[counter].append(nhisp[i])
        counter+=1
        i+=1

    headers = ['Jurisdiction Name', 'Number of Hispanic Residents']
    print tabulate.tabulate(arr, headers=headers)

#This builds a table that displays the raw data that we collected from nycdemographics.rdf and prints it to the screen.

def buildTable2(cdeaths, ethnicity, ndeaths):

    i = 0
    counter = 0
    arr = []
    while i < len(cdeaths):
        arr.append([])
        arr[counter].append(cdeaths[i])
        arr[counter].append(ethnicity[i])
        arr[counter].append(ndeaths[i])
        counter+=1
        i+=1

    headers = ['Cause of Death','Ethnicity of Victim', 'Number of Deaths']
    print tabulate.tabulate(arr, headers=headers)

    return arr

#This aggregates the data that we collected from nycdeaths.rdf and displays them in a table.

def buildTable3(dict):

    table = [(v, k) for k, v in dict.iteritems()]
    headers = ['Number of Deaths', 'Cause of Death']
    print tabulate.tabulate(table, headers=headers)

#This sorts and displays the aggregated death counts to easily find the leading causes.    
def buildTable4(arr):

    sorted_arr = sorted(arr, key=lambda x: int(x[2]), reverse=True)
    new_cdeath = []
    new_ndeath = []
    counter = 0

    while counter < len(sorted_arr):
        new_cdeath.append(sorted_arr[counter][0])
        new_ndeath.append(sorted_arr[counter][2])
        counter +=1

    tups= zip(new_cdeath,new_ndeath)

    dict = defaultdict(int)
    for (x, y) in tups:
        dict[x] += int(y)

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

    print("\n Just Hispanics now:\n")

    headers = ['Number of Deaths', 'Cause of Death']
    print tabulate.tabulate(sorted_dict, headers=headers)

#This aggregates the list of residents from the census data so that we can calculate totals and averages
#It returns a list containing the result.
def aggregateResidents(list):

    aggregated = []
    total = 0
    i = 0
    while i < len(list):
        total +=int(list[i])
        i += 1


    aggregated.append(total)

    return aggregated

#This returns the aggregated number of deaths from nycdeaths.rdf
def aggregateDeaths():

    a= []
    with open("nycdeaths.rdf", 'r') as file:
        for i in file:
            if "<ds:count>" in i:
                x = stripTags(i,"<ds:count>","</ds:count>")
                a.append(x)
    aggregate = 0
    for i in a:
        aggregate +=int(i)

    return aggregate


#This aggregates the causes in order to be able to calculate totals
def aggregateCauses(cdeaths,ndeaths):

    tups =zip(cdeaths,ndeaths)

    dict = defaultdict(int)
    for (x, y) in tups:
        dict[x] += int(y)

    return dict

def main():

    nhisp = getDemographics()
    jname = getJurisdiction()
    cdeaths = getDeathCause()
    ethnicity = getEthnicity()
    ndeaths = getDeathCount()


    t_hisp_deaths = aggregateDeaths()
    tethnicity = aggregateResidents(nhisp)


    print("\nRaw Data:\n")
    buildTable1(jname, nhisp)
    arr = buildTable2(cdeaths, ethnicity, ndeaths)
    blah = getHispDeaths(arr)

    ag = aggregateCauses(cdeaths,ndeaths)
    
    print("\nAggregated Data:\n")
    buildTable3(ag)
    buildTable4(blah)

    print("\nTotal Deaths:\n")
    print (t_hisp_deaths)
    print ("Percent of Hispanic deaths from homicides\n")
    print(float(296)/int(t_hisp_deaths))



main()