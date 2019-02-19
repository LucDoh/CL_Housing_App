import sys
import os.path
import subprocess
from scripts import analyzePosts, clHousingScraper
from utils import makePdf

def main():
    prefix, zip, dist, n = str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), int(sys.argv[4])
    stringDB = 'clHousing_' + zip + "_" + dist + "_" + str(n) + ".db"
    b = os.path.isfile('dbs/' + stringDB)

    #1 Scrape if data doesn't exist
    if b == False: stringDB = clHousingScraper.scrapeRentals(prefix, zip, dist, n)
    #2 Analyze
    analyzePosts.analyze(stringDB)

    #3 Generate report in pdf form.
    makePdf.generateReport('plots/facts.txt','plots/distPlots.png', 'plots/relPlot.png')

if __name__== "__main__":
  main()













    #stringDB = 'clHousing_20740_5_240.db'
