import sys
from scripts import analyzePosts, clHousingScraper

def main():

    prefix = str(sys.argv[1]) #washingtondc
    zip = str(sys.argv[2]) #20740
    dist = str(sys.argv[3]) #5
    n = int(sys.argv[4])
    #1
    stringDB = clHousingScraper.scrapeRentals(prefix, zip, dist, n)
    #2
    analyzePosts.analyze(stringDB)

if __name__== "__main__":
  main()
