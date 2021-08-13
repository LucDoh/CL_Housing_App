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
from helpers import makeSoup, getHouses, storeInSQL, addtlInfo, retrieveAll

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import sys

# To run analysis, run with first argument the db containing df of rentals
# df.columns = ['PID', 'Title', 'Price', 'BR', 'Sqft', 'Link', 'Ba', 'Lat', 'Long', 'Description']
def main():
    # 1) Retrieve data from db
    stringDB = 'dbs/' + sys.argv[1] #'clHousing_02-14-18.db'
    dfx = retrieveAll(stringDB) #print(dfx.dtypes)
    dfx = removeOutliers(dfx)

    # 2) Trains a linear regression algo to make predictions of Sqft by Price
    runLinRegr = False
    if(runLinRegr): makeLinearRegr(dfx, False)
    # 3) Plots distributions of Price, BR, + computes average rentals
    plotIt(dfx)



    # Folium heatmap, where the temperature is the price/sqft
def makeMap(dfx):
        hmdata = []
        for index, row in dfx.iterrows():
            hmdata.append([row['Lat'], row['Long'],row['PricePerSqft']])
        m = folium.Map(location=[38.9869, -76.9426],tiles='stamentoner', zoom_start=10.9)
        HeatMap(hmdata).add_to(m)
        m


def removeOutliers(dfx):
    #print("Unique BR: " + str(dfx.BR.unique()))
    sizePre = dfx.Price.values.size
    print("Outliers (>7*STD) being removed")
    dfx = dfx[dfx.Price/dfx.BR > 300] #Only keep if Price/BR > 300. Not wisconsin.
    #dfx =  dfx[np.abs(dfx.Price-dfx.Price.mean()) <= (5*dfx.Price.std())]
    dfx =  dfx[np.abs(dfx.Sqft-dfx.Sqft.mean()) <= (7*dfx.Sqft.std())]
    print('# of listings: ' + str(sizePre) + ' --> ' + str(dfx.Price.values.size))
    #print("Unique BR: " + str(dfx.BR.unique()))
    return dfx


def plotIt(dfx):
    perBRAvg = []
    for i in range (1, int(dfx.BR.max())+1):
        x = dfx[dfx.BR == i]
        x_mean = round(dfx[dfx.BR == i].Price.mean(),2)
        perBRAvg.append(round(x_mean/i, 2))
        print ("Average for %s bedrooms is $%0.2f. --> %0.2f per room [%s]"
            % (i, x_mean, x_mean/i, len(dfx[dfx.BR==i].index)))

    import warnings; warnings.filterwarnings("ignore", category=FutureWarning) #TBFixed
    #Seaborn plotting
    sns.set(style="ticks")
    sns.relplot(x="Sqft", y="Price", hue="BR", palette="ch:r=-1.5,l=.75", data=dfx[dfx.BR < 5]);#palette="ch:r=-.5,l=.75",

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    s1 = pd.Series(dfx.BR.values, name='Bedrooms'); s2 = pd.Series(dfx[dfx.BR == 2].Price.values, name="Price of 2BR")
    s3 = pd.Series(perBRAvg, name = "Mean Price/BR"); s4 = pd.Series(np.arange(1, int(dfx.BR.max()) + 1), name='# of BRs')
    sns.distplot(s1, kde=False, bins=np.arange(0,7), norm_hist=False, ax=ax1)
    sns.barplot(x=s4, y = s3, ax = ax2)
    sns.distplot(dfx.Price.values.astype('float64'), axlabel = "Price", ax = ax3)
    sns.distplot(s2, kde = False, ax = ax4)

    plt.show()


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

if __name__== "__main__":
  main()





# GRAVEYARD
'''
print(dfx.columns)
print(dfx.iloc[0])
print(dfx.iloc[5])
print(dfx.Price.size)
print(dfx.Title.unique().size)
print(dfx.PricePerSqft.unique().size)
'''

'''
# What do the distribution of rental prices look like?
#sns.distplot(dfx.Price)
print("Average rental price in College Park: " + str(dfx.Price.mean()))
print("Max rental price: " + str(dfx.Price.max()))
print("Min rental price: " + str(dfx.Price.min()))
sns.distplot(dfx.Price)
plt.show()
#sns.distplot((df.PricePerSqft))
print("Median rental price/sqft in College Park: " + str(dfx.PricePerSqft.median()))
plt.show()
# What about distribution of Bedrooms?
sns.distplot(dfx.BR)

sns.heatmap(dfx.corr(), annot=True, fmt=".2f")

# Folium heatmap, where the temperature is the price/sqft
hmdata = []
for index, row in dfx.iterrows():
    hmdata.append([row['Lat'], row['Long'],row['PricePerSqft']])
m = folium.Map(location=[38.9869, -76.9426],tiles='stamentoner', zoom_start=10.9)
HeatMap(hmdata).add_to(m)
m
'''
