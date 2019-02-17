# Overview

The whole rental analysis program is run by one script: runAll.py which will scrape craigslist within some radius, r, of a zip-code for n rentals.

`python runAll.py washingtondc 20740 5 3000`

## Input arguments:

    arg1: the craigslist prefix  [washingtondc]
    arg2: zipcode                [20740]
    arg3: radius in miles        [5]
    arg4: number of posts        [3000]
---------------------------------------------------


## Outputs:   

a) A SQLite database containing a pandas dataframe of all rentals called *clHousing_zip_radius_n.db*. --> stored in **./dbs/**

b) 5 plots as pngs --> stored in **./plots/**

-----------------------------------------------------------
