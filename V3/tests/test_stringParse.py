import requests
from bs4 import BeautifulSoup
import re
link = 'https://orangecounty.craigslist.org/search/apa?postal=92697&search_distance=5'
r = requests.get(link)
soup = BeautifulSoup(r.content, 'lxml');
sum = 0
sum_got = 0
for row in soup.find_all(class_="result-row"):
    sum = sum + 1
    try:
        r = row.find(class_='housing').text.splitlines() # for each row, grab BR + SQFT
    #Removes whitespace/empty line elements
        brSqft = [i.replace(" ",'').replace('-','') for i in r if re.search('[a-zA-Z]', i)]
    except AttributeError:
        brSqft = [float('nan'), float('nan')]
    if(len(brSqft)== 1 and ('br' in brSqft[0])):
        brSqft = brSqft + [float('nan')]
    elif(len(brSqft) == 1):
        brSqft = [float('nan')] + brSqft

    #print(r)
    if(len(brSqft) == 2):
        sum_got = sum_got + 1

print("Num rows: " + str(sum))
print("Sum got: " + str(sum_got))




'''
    brSqft = [i.replace(" ",'').replace('-','') for i in r if not (i.isspace()) and i != '']
    #If number of bedrooms OR Sqft is N/A, make it nan
    if(len(brSqft)==1):
        if(brSqft[0].contains('br')):
            brSqft = brSqft + [float('nan')]
        else:
            brSqft = [float('nan')] + brSqft
'''
