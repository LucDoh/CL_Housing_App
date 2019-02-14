import requests
from bs4 import BeautifulSoup
#import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from helpers import makeSoup, getHouses, storeInSQL, addtlInfo, retrieveAll

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
stringDB = 'clHousingA.db'
dfx = retrieveAll(stringDB)

reg = LinearRegression()
M = dfx.Price.values
X =  dfx.Price.values.reshape(-1,1)#.reshape(-1,1)
y = dfx.Sqft.values.reshape(-1,1)
print(X.shape) #192
X_train = X[:91]
y_train = y[:91]
X_test = X[91:]
y_test = y[91:]
reg.fit(X_train, y_train)
reg.score(X_train, y_train)
reg.coef_, reg.intercept_
y_pred = reg.predict(X_test)

print('Coefficients: \n', reg.coef_)

print('Variance score: %.2f' % r2_score(y_test, y_pred))
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
#print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
#plt.scatter(X, y,  color='black')
#plt.scatter(X_train, y_train,  color='black')
plt.scatter(X_test, y_test,  color='red')
plt.scatter(X_test, y_pred,  color='red')
#plt.plot(X_test, y_pred, color='blue')

plt.xticks(())
plt.yticks(())

plt.show()




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
