import requests
from bs4 import BeautifulSoup

r = requests.get('https://newyork.craigslist.org/brk/abo/d/brooklyn-bedstuyspacious-3br-aptprime/6821145013.html')
soup = BeautifulSoup(r.content, 'lxml');
s = soup.find(id="map")
print(s.text)
lat = s.get('data-latitude')
print(lat)
