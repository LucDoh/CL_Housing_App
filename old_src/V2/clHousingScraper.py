import requests
import sys

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns

from helpers import makeSoup, getHouses, storeInSQL, addtlInfo, cleanRow, pricePerSqft
from distFromPOI import getDistances

# This scraper grabs all postings, making a data frame called df whose rows
# are rentals, of  the form:
# ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link', 'Ba', 'Lat', 'Long', 'Description']
def main():
    distCalc = False
    prefix = str(sys.argv[1]) #washingtondc
    zip = str(sys.argv[2]) #20740
    dist = str(sys.argv[3]) #5
    n = int(sys.argv[4])
    stringDB = 'clHousing_' + zip +"_" + dist +".db" #Name the db it will be stored in
    searchDist = dist
    df = pd.DataFrame() #strkey = ''

    startingLink = 'https://' + prefix +'.craigslist.org/search/apa?availabilityMode=0&postal=' + zip + '&search_distance=' + searchDist
    link = startingLink
    #Max results in craigslist for any search always appears to stop at 3000
    for i in range(0,n,120): #3000 is the max
        if(i!=0):
            strkey = 's=' + str(i)
            link = 'https://' + prefix + '.craigslist.org/search/apa?availabilityMode=0&postal=' + zip + strkey + '&search_distance=' + searchDist
        df_current = getHouses(makeSoup(link))
        df = df.append(df_current, ignore_index=True)

    print(df.size)   # We have 2034 when running over 3 pages of cl
    print(df.iloc[0]) # 339 rows x 6 cols

    df.columns = ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link'] #Name the columns

    #Let's make new columns:
    df['Ba'] = None
    df['Lat'] = None
    df['Long'] = None
    df['Description'] = None
    df[['Ba','Lat', 'Long', 'Description']] = df.apply(addtlInfo, axis=1)

    if(distCalc == True):
        #Let's make 2 new columns:
        df2['UMD-distance'], df2['Metro-distance'] = None, None
        df2[['UMD-distance', 'Metro-distance']] = df2.apply(getDistances, axis=1)

    #Clean-up data, removing extra characters & adding a col for price/sqft
    df[['Price','BR', 'Ba', 'Sqft']] = df.apply(cleanRow, axis=1)
    print(df.iloc[0])
    print(df.iloc[10])
    df.columns = ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link', 'Ba', 'Lat', 'Long', 'Description']#, 'UMDDistance', 'MetroDistance']
    df['PricePerSqft'] = None
    df['PricePerSqft'] = df.apply(pricePerSqft,axis=1)
    df = df.drop(df[(df['Price'] > 10000)  | (df['Price'] < 200)].index) #Remove outliers

    # Store it all in a SQLite db titled stringDB
    stringDB = 'dbs/' + stringDB
    storeInSQL(df, stringDB)

main()
