import requests
from bs4 import BeautifulSoup
import re
#import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine


def makeSoup(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml');
    return(soup)

# LETS GET SOME ATTRIBUTES
# Using a BeautifulSoup object, we extract in our first pass the relevant information on the posting that can be obtained
# before visiting the link.
#2nd, better version
def getHouses(soup):
    sum_Unlabeled = 0
    r_matrix = []
    for row in soup.find_all(class_="result-row"):
        pID = row.get('data-pid')
        rtitle = row.find(class_="result-title hdrlnk") #Grabs post title + href
        rtitle_txt = rtitle.text
        href = rtitle.get('href')
        date = row.find(class_="result-date").get('datetime') #2018-12-11 13:57
        if row.find(class_='result-price') is None:  #if price is empty
            price = 'nan'
        else:
            price = row.find(class_='result-price').text

        ## brSqft = getBrSqft(row)
        try:
            r = row.find(class_='housing').text.splitlines() # for each row, grab BR + SQFT
            brSqft = [i.replace(" ",'').replace('-','') for i in r if re.search('[a-zA-Z]', i)]  #clean strs
            #print(brSqft)
        except AttributeError:
            brSqft = [float('nan'), float('nan')]
        if(len(brSqft)== 1 and ('br' in brSqft[0])):
            brSqft = brSqft + [float('nan')]
        elif(len(brSqft) == 1):
            brSqft = [float('nan')] + brSqft
        ###
        r_matrix.append([pID, rtitle_txt, price] + brSqft + [href])

    df = pd.DataFrame(r_matrix)
    print("Scraping a page... " + str(sum_Unlabeled) + " misses")
    return(df)

# Grab additional info from Link (Ba, lat, long, description)
def addtlInfo(row):
    r = requests.get(row['Link'])
    soup = BeautifulSoup(r.content, 'lxml');
    # In RARE posts, parser won't find a map id and return none
    s = soup.find(id="map")
    if s is None: return pd.Series(['nan', 'nan', 'nan', 'nan'])
    lat, long = s.get('data-latitude'), s.get('data-longitude') # Sometimes they don't have a lat/long?
    description = soup.find(id='postingbody').text

    s_2 = soup.find(class_='shared-line-bubble') # B) The first shared-line-bubble tag usually gives br/ba.
    # If br/ba isn't included, s_2 will yield next shared-line-bubble: availability date.
    # We don't care about this, so we'll set the number of Baths to nan
    if (s_2 is not None and 'Ba' in s_2.text):
        baths = s_2.text.split("/")[1]
    else:
        baths = 'nan'

    return pd.Series([baths, float(lat), float(long), description])

def pricePerSqft(row):
    row['PricePerSqft'] = row['Sqft']/row['Price']
    return pd.Series([row['PricePerSqft']])

#Store in SQLite
#Super basic example of how to write to a SQLite DB
def storeInSQL(df,stringDB):
    engine = create_engine('sqlite:///' + stringDB) # Creat new database if it doesn't already exist
    connection = engine.connect() # Connect to the database
    df.to_sql('Listings', con=engine, if_exists='replace')

def retrieveAll(stringDB):
    #And to query this database, we write our query in SQL and then use the pandas read_sql function
    engine = create_engine('sqlite:///' + stringDB) # Creat new database if it doesn't already exist
    connection = engine.connect() # Connect to the database
    df_SQL = pd.read_sql("SELECT * FROM Listings", connection)
    return df_SQL

# Now we can remove the unwanted characters using pythons replace function as well as cast
# the data to the appropriate type. While we're here, let's also round our distance columns
# to the 2nd decimal place!
def cleanRow(row):
    row['BR'] = float(str(row['BR']).replace("br", "")) if row['BR'] is not 'nan' else float('nan')
    row['Sqft'] = float(str(row['Sqft']).replace("ft2", "")) if row['Sqft'] is not 'nan' else float('nan')
    row['Price'] = float(str(row['Price']).replace("$","")) if row['Price'] is not 'nan' else float('nan')

    if ('Ba' in row['Ba']):
        try:
            row['Ba'] = float(row['Ba'].replace("Ba", ""))
        except:
            row['Ba'] = float(0.5) # It's shared and comes up as sharedBa
    #row['UMD-distance'] = round(float(row['UMD-distance']), 2)
    #row['Metro-distance'] = round(float(row['Metro-distance']), 2)

    return pd.Series([row['Price'],row['BR'], row['Ba'], row['Sqft']])#, row['UMD-distance'], row['Metro-distance']])
