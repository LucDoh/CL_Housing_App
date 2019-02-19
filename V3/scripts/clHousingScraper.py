import requests
import sys

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns

from utils.helpers import makeSoup, getHouses, storeInSQL, addtlInfo, cleanRow, pricePerSqft
#from utils.distFromPOI import getDistances

# This scraper grabs all postings, making a data frame called df whose rows
# are rentals, of  the form:
# ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link', 'Ba', 'Lat', 'Long', 'Description']
def scrapeRentals(prefix, zip, dist, n):
    distCalc = False
    stringDB = 'clHousing_' + zip + "_" + dist + "_" + str(n) + ".db" #Name the db it will be stored in

    tag = 'apa'
    link = 'https://' + prefix +'.craigslist.org/search/' + tag + '?availabilityMode=0&postal=' + zip + '&search_distance=' + dist
    #switch tag (NY uses aap for some reason)
    if(requests.get(link).status_code == 404): tag = 'aap'
    #Iterate through pages in craigslist to get n listings
    ####
    df =  getnListings(prefix, zip, dist, n, link, tag) # get all apts and houses
    df.columns = ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link'] #Name the columns
    print((df['Title'].value_counts()[0])) #??? getNListings yields too many dupes
    '''
    dfr = getnListings(prefix, zip, dist, n, link, 'roo') # get all rooms
    dfr.columns = ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link']
    dfr['BR'] = "1br"
    print(dfr.columns)
    print(dfr.to_string())
    print(dfr.iloc[:4])
    #print(df.iloc[:4])
    print ("Before join, length is " + str(len(df.index)))
    df = df.append(dfr, sort=False)
    '''
    ###

    print("Total # of rentals  " + str(len(df.index)))   # We have 2034 when running over 3 pages of cl

    #Let's make new columns and scrape this additional info from the posting itself
    df['Ba'], df['Lat'], df['Long'], df['Description'] = None, None, None, None
    df[['Ba','Lat', 'Long', 'Description']] = df.apply(addtlInfo, axis=1)

    if(distCalc == True): #Let's make 2 new columns:
        df2['UMD-distance'], df2['Metro-distance'] = None, None
        df2[['UMD-distance', 'Metro-distance']] = df2.apply(getDistances, axis=1)

    #Clean-up data, removing extra characters & adding a col for price/sqft
    sizePre = len(df.index)
    df.dropna(how='all')
    print('Initial size:' + str(sizePre) + '. After removing Nonetype rows: ' + str(len(df.index)))

    df[['Price','BR', 'Ba', 'Sqft']] = df.apply(cleanRow, axis=1)
    df.columns = ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link', 'Ba', 'Lat', 'Long', 'Description']#, 'UMDDistance', 'MetroDistance']
    df['PricePerSqft'] = None
    df['PricePerSqft'] = df.apply(pricePerSqft,axis=1)
    df = df.drop(df[(df['Price'] > 10000)  | (df['Price'] < 200)].index) #Remove outliers

    # Store it all in a SQLite db titled stringDB
    stringDB_2 = 'dbs/' + stringDB
    storeInSQL(df, stringDB_2)
    return stringDB

def getnListings(prefix, zip, dist, n, link, tag):
    df = pd.DataFrame()
    for i in range(0,n,120): #3000 is the max
        if(i!=0):
            strkey = 's=' + str(i)
            link = 'https://' + prefix + '.craigslist.org/search/' + tag +'?availabilityMode=0&postal=' + zip + strkey + '&search_distance=' + dist
        df_current = getHouses(makeSoup(link))
        df = df.append(df_current, ignore_index=True)
    return df
