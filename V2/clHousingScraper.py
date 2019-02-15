import requests
from bs4 import BeautifulSoup
#import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import seaborn as sns

from helpers import makeSoup, getHouses, storeInSQL, addtlInfo, cleanRow, pricePerSqft
from distFromPOI import getDistances

# This part grabs all postings
#Create empty df for all house postings
# Makes a data frame called df whose rows are housing postings, of form:
# df.columns = ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link', 'Ba', 'Lat', 'Long', 'Description']
def main():
    distCalc = False
    stringDB = 'clHousing_QQQ' #Name the db it will be stored in
    searchDist = 5
    df = pd.DataFrame() #strkey = ''
    startingLink = 'https://washingtondc.craigslist.org/search/apa?availabilityMode=0&postal=20740&search_distance='+ str(searchDist)
    link = startingLink
    #Max results in craigslist for any search always appears to stop at 3000
    for i in range(0,3000,120): #3000 is the max
        if(i!=0):
            strkey = 's=' + str(i)
            link = 'https://washingtondc.craigslist.org/search/apa?availabilityMode=0&postal=20740&' + strkey + '&search_distance=' + str(searchDist)
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
    storeInSQL(df, stringDB)
main()
