#Import all the relevant packages
import requests
from bs4 import BeautifulSoup
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import seaborn as sns
from haversine import haversine

# We'll use the haversine formula here and add the new data as  new columns
# 'UMD-distance' & 'Metro-distance'

umd = (38.9869, -76.9426)
# CP, Greenbelt, PG Plaza, New Carrollton, Silver Spring, Takoma, Fort Totten Metro locations
metros = [(38.9780, -76.9287), (39.0110, -76.9111), (38.9651, -76.9564), (38.9478, -76.8719),
         (38.9931, -77.0283), (38.9755, -77.0178), (38.9518, -77.0022)]

# We'll define 2 helper functions get compute the new columns
def calculateMetroDistance(l1): # ((long1, lat1), (long2, lat2))
    md = 10000
    #There is certainly a more pythonic and efficient way to do this!
    for m in metros:
        d = haversine(l1, m, unit='mi')
        if(d < md):
            md = d
    return md

def getDistances(row):

    # Get longitude & longitude
    longlat = (row['Lat'], row['Long'])
    umdist = haversine(longlat, umd)
    mdist = calculateMetroDistance(longlat)
    #Return distance to umd and distance to nearest metro (miles)
    return pd.Series([str(umdist), str(mdist)])
