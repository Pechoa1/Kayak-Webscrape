The goal of this project was to create a webscraper in python that would pull data from Kayak.com 
Once the data is scraped it is organzied in a dataframe for later analysis such as finding the best time fly when related to price.

The code uses selenium and beautiful soup to pull data from the desired webpage.
we begin by setting up selenium and defining departures, dates, etc to send to the link we will explore.
Then a function (load_more()) is defined which will naviage to the more results button and click it. This was built to work for a static or dynamic page

following, beautiful soup along with regex to scrape the data points.

finally, the data was formatted to have same length, then put into a pandas data frame

This code can be ran from ones pc, though using the path to chromedriver will need to be adjusted.
