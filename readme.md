# Overview of V3

The whole rental analysis program is run by the script runAll.py, which will:

1. Scrape craigslist within some radius, r, of a zip-code for n rentals. If a database fulfilling the requests already exists, this is skipped.
2. Plot & compute, after calling removeOutliers() to removes posts with no price or where the price is >5*STD from the mean.
3. Generate a PDF report of the rental market, in plots/report.pdf

---------------------------------------------------

## Running an example:
`python runAll.py washingtondc 20740 5 3000`

---------------------------------------------------
## Input arguments:

    arg1: the craigslist prefix  [washingtondc]
    arg2: zipcode                [20740]
    arg3: radius in miles        [5]
    arg4: number of posts        [3000]
---------------------------------------------------
## Outputs:   

A) A SQLite database containing a pandas dataframe of all rentals called *clHousing_zip_radius_n.db* (stored in **./dbs/**).

B)  A PDF report of the average price by # of bedrooms and 5 distribution plots.
**./plots/**

-----------------------------------------------------------

## Example report for Mountain View, CA 94039:

<p align="center">
Here is the report for <i> clHousing_94039_5_3000.db </i> with <b> 2500 listings </b>. <br/> <br/>
Average for 1 bedrooms is $2965.17. --> $2965.17 per room&nbsp;&nbsp;&nbsp;[875 listings] <br/>
Average for 2 bedrooms is $3668.39. --> $1834.19 per room&nbsp;&nbsp;&nbsp;[1400 listings] <br/>
Average for 3 bedrooms is $4812.89. --> $1604.30 per room&nbsp;&nbsp;&nbsp;[225 listings]
</p>
<p align="center">
  <img src="V3/plots/nice_MountainView/distPlots.png" />
</p>
<p align="center">
  <img src="V3/plots/nice_MountainView/relPlot.png" />
</p>
