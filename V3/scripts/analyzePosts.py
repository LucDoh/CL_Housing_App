import requests
from bs4 import BeautifulSoup
#import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#import folium
#from folium.plugins import HeatMap
from utils.helpers import retrieveAll, storeInSQL

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import sys

# To run analysis, run with first argument the db containing df of rentals
# df.columns = ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link', 'Ba', 'Lat', 'Long', 'Description']
def analyze(stringDB):
    print("Here is the report for " + stringDB +".", file=open("plots/facts.txt", "w"))

    # 1) Retrieve data from db
    stringDB = 'dbs/' + stringDB #'clHousing_02-14-18.db'
    dfx = retrieveAll(stringDB)
    dfx = removeOutliers(dfx)
    # 2) Trains a linear regression algo to make predictions of Sqft by Price
    runLinRegr = False
    if(runLinRegr): makeLinearRegr(dfx, False)
    # 3) Plots distributions of Price, BR, + computes average rentals
    plotIt(dfx)
    print("Report for: " + stringDB + " is in plots/facts.txt.")
    #print(dfx.dtypes)




def removeOutliers(dfx):
    sizePre = dfx.Price.values.size
    dfx = dfx.dropna(subset=['Price']) # Drop NaNs
    #dfx = dfx[dfx.Price/dfx.BR > 300] #Only keep if Price/BR > 300. Not wisconsin.

    print("NaNs being removed... %s%%  NaNs (Price)." %
        ((len(dfx['Price'].index) - len(dfx['Price'].dropna().index))/len(dfx['Price'])))
    print("Outliers (Price>5*STD) being removed...")
    dfx =  dfx[np.abs(dfx.Price-dfx.Price.mean()) <= (5*dfx.Price.std())]
    print('# of listings: ' + str(sizePre) + ' --> ' + str(dfx.Price.values.size))
    print('(' + str(dfx.Price.values.size) + ' listings)\n', file=open("plots/facts.txt", "a"))


    return dfx


def plotIt(dfx, savePlot = True):
    perBRAvg = []
    for i in range (1, int(dfx.BR.max())+1):
        x = dfx[dfx.BR == i]
        x_mean = round(x.Price.mean(),2)
        perBRAvg.append(round(x_mean/i, 2))
        if not np.isnan(x_mean):
            print ("Average for %s bedrooms is $%0.2f. --> $%0.2f per room [%s]"
            % (i, x_mean, x_mean/i, len(dfx[dfx.BR==i].index)), file=open("plots/facts.txt", "a"))

    #Seaborn plotting
    import warnings; warnings.filterwarnings("ignore", category=FutureWarning) #TBFixed
    sns.set(style="ticks")

    sns.relplot(x="Sqft", y="Price", hue="BR",
        palette="ch:r=-1.5,l=.75", data=dfx[dfx.BR < 5]);#palette="ch:r=-.5,l=.75",
    if (savePlot == True): plt.savefig('plots/relPlot.png')
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11,7))

    sBR = pd.Series(dfx.BR.values, name='Bedrooms');
    sns.distplot(sBR, kde=False, bins=np.arange(0,7), ax=ax1)
    sMeanPBr = pd.Series(perBRAvg, name = "Mean Price by BR");
    sNumBr = pd.Series(np.arange(1, int(dfx.BR.max()) + 1), name='# of BRs')

    sns.barplot(x=sNumBr, y = sMeanPBr, ax = ax2)
    sns.distplot(dfx.Price.values.astype('float64'), axlabel = "Price (rentals)", ax = ax3)

    sns.distplot(dfx.dropna(subset=['Sqft']).Sqft.values.astype('float64'), axlabel = "Sqft (rentals)", ax = ax4)
    if (savePlot == True): plt.savefig('plots/distPlots.png')
    plt.show()
    #s2BR = pd.Series(dfx[dfx.BR == 2].Price.values, name="Price of 2BRs")
    #sns.distplot(s2BR, kde = False, ax = ax4)

# Folium heatmap, where the temperature is the price/sqft
def makeMap(dfx):
        hmdata = []
        for index, row in dfx.iterrows():
            hmdata.append([row['Lat'], row['Long'],row['PricePerSqft']])
        m = folium.Map(location=[38.9869, -76.9426],tiles='stamentoner', zoom_start=10.9)
        HeatMap(hmdata).add_to(m)
        m


        # Perform linear regression, predict Price from sqft
def makeLinearRegr(dfx, boolPlot = False):
    reg = LinearRegression()
    X =  dfx.Price.values.reshape(-1,1) # reshapes into nx1 2D array
    y = dfx.Sqft.values.reshape(-1,1)
    print(X.shape)

    X_train = X[:950]
    y_train = y[:950]
    X_test = X[950:]
    y_test = y[950:]
    reg.fit(X_train, y_train)
    reg.score(X_train, y_train)
    reg.coef_, reg.intercept_
    y_pred = reg.predict(X_test)

    print('Coefficients: \n', reg.coef_)
    print('Variance score: %.2f' % r2_score(y_test, y_pred)) # 1 is perfect prediction
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))

    if (boolPlot):
        plt.scatter(X_test, y_test,  color='red')
        plt.plot(X_test, y_pred, color='blue')
        plt.xticks(())
        plt.xlabel("Price")
        plt.show()


# GRAVEYARD
'''
# What do the distribution of rental prices look like?
sns.distplot(dfx.Price)
#sns.distplot((df.PricePerSqft))
print("Max/Min rental price: %s, %s" % (str(dfx.Price.max()), str(dfx.Price.min())))
print("Median rental price/sqft in College Park: " + str(dfx.PricePerSqft.median()))
# What about distribution of Bedrooms?
sns.distplot(dfx.BR)
sns.heatmap(dfx.corr(), annot=True, fmt=".2f")
'''
