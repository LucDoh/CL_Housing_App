import requests
from bs4 import BeautifulSoup
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
def getHouses(soup):
    sum_Unlabeled = 0
    r_matrix = []
    for row in soup.find_all(class_="result-row"):
        #Try catch Nonetype object error (can't call .text)
        try:
            pID = row.get('data-pid')
            rtitle = row.find(class_="result-title hdrlnk") #Grabs post title + href
            rtitle_txt = rtitle.text
            price = row.find(class_='result-price').text
            href = rtitle.get('href')
            date = row.find(class_="result-date").get('datetime') #for each row, grab - 2018-12-11 13:57
            r = row.find(class_='housing').text.splitlines() # for each row, grab BR + SQFT
            #Removes whitespace/empty lines
            brSqft = [i.replace(" ",'').replace('-','') for i in r if not (i.isspace()) and i != '']
            #If number of bedrooms OR Sqft is N/A, make it nan
            if(len(brSqft)==1):
                if(brSqft[0].contains('br')):
                    brSqft = brSqft + [float('nan')]
                else:
                    brSqft = [float('nan')] + brSqft

            r_matrix.append([pID, rtitle_txt, price] + brSqft + [href])
            #print(brSqft)
        except:
            sum_Unlabeled+=1 #Catch value error, some don't have text
    df = pd.DataFrame(r_matrix)
    #print(df.shape)
    #print("Number of ^bad^ rows: " + str(sum_Unlabeled))
    return(df)

# Grab additional info from Link (Ba, lat, long, description)
def addtlInfo(row):
    r_test = requests.get(row['Link'])
    soup_test = BeautifulSoup(r_test.content, 'lxml');
    s = soup_test.find(id="map")
    lat, long = s.get('data-latitude'), s.get('data-longitude') # A) For longitude & longitude
    s_2 = soup_test.find(class_='shared-line-bubble') # B) The first shared-line-bubble tag usually gives br/ba.
    # BUT, if br/ba isn't included, then the s_2 will return the next shared-line-bubble: availability date. We don't care about
    # this, so we'll set the number of Baths to nan in that case
    if ('Ba' in s_2.text):
        baths = s_2.text.split("/")[1]
    else:
        baths = 'nan'
    description = soup_test.find(id='postingbody').text # c) Description
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
    row['BR'] = int(row['BR'].replace("br", ""))
    #row['Ba'] = row['Ba'].replace("Ba", "")# Can't be converted to float as some say 'shared'.replace(" ",""))
    #TRY :
    if ('Ba' in row['Ba']):
        try:
            row['Ba'] = float(row['Ba'].replace("Ba", ""))
        except:
            row['Ba'] = float(0.5) # It's shared and comes up as sharedBa
    #else:
    #    row['Ba'] = float(np.NaN)
    row['Sqft'] = int(row['Sqft'].replace("ft2", ""))
    row['Price'] = float(row['Price'].replace("$",""))
    #row['UMD-distance'] = round(float(row['UMD-distance']), 2)
    #row['Metro-distance'] = round(float(row['Metro-distance']), 2)

    return pd.Series([row['Price'],row['BR'], row['Ba'], row['Sqft']])#, row['UMD-distance'], row['Metro-distance']])
