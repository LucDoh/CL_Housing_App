This V2 is meant to be run in two parts:

1) The scraper is run by: 'python clHousingScraper.py arg1 arg2 arg3 arg4', where
      arg1: the craigslist prefix  [washingtondc]
      arg2: zipcode [20740]
      arg3: radius in miles [5]
      arg4: number of posts [3000]
Output: A database of the form clHousing_zip_radius.db, containing a pandas dataframe of all rentals.
------

2) The analysis portion is run by providing the db containing df of rentals:
'python analyzePosts.py clHousing_20740_5.db'

Output: 4 plots
------
