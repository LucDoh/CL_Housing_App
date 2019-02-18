# Overview of V3

The whole rental analysis program is run by the script runAll.py, which will:

1. Scrape craigslist within some radius, r, of a zip-code for n rentals. If a database fulfilling the requests already exists, this is skipped.
2. Plot & compute, after calling removeOutliers() to removes posts with no price or where the price is >5*STD from the mean.
3. Generate a PDF report of the rental market, in plots/report.pdf

## Running an example
`python runAll.py washingtondc 20740 5 3000`

## Input arguments:

    arg1: the craigslist prefix  [washingtondc]
    arg2: zipcode                [20740]
    arg3: radius in miles        [5]
    arg4: number of posts        [3000]
---------------------------------------------------


## Outputs:   

A) A SQLite database containing a pandas dataframe of all rentals called *clHousing_zip_radius_n.db* (stored in **./dbs/**).

B) 5 plots as pngs

C) Text file with averages

D) A PDF report of B and C, stored in **./plots/**

-----------------------------------------------------------
