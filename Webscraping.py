# idea: Scrape flight data from a website then return the fastest and cheapest result
# this will be done for dates and cities defined by the user

# selenuim imports and bsoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import lxml

# Pandas and data structure
import pandas as pd
import numpy as np

# extra packages
from time import sleep, strftime

# set up path to web driver and call the path to driver variable
PATH = "C:\Webdrivers\chromedriver.exe"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# open window
driver = webdriver.Chrome(PATH, options=chrome_options)

# variables for flight data
departure = 'CHI'  # Chicago
arrival = 'MIA'  # Miami
departure_date = '2023-05-05'  # YYYY-MM-DD
arrival_date = '2023-05-10'
flexibility_option = "flexible"  # for +/= [1,3] days
number_of_days = "3days"  # can be 1-3 days

# get Kayak webpage and open
kayak = f"https://www.kayak.com/flights/{departure}-{arrival}/{departure_date}-{flexibility_option}-{number_of_days}/{arrival_date}-{flexibility_option}-{number_of_days}"
driver.get(kayak)
print(driver.title)
sleep(10)


# function to load more page results
def load_more():
    i = 25
    # static page
    while i > 0:
        try:
            stat_load = driver.find_element("xpath", more_results)
            stat_load.click()
            print("Ran static")
            sleep(5)
            i -= 1
        except:
            print("None static Xpath")
            break
    # dynamic page
    while i > 0:
        try:
            dynamic_results = '/html/body/div[1]/div[1]/main/div/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/div/div'
            dyn_load = driver.find_element("xpath", dynamic_results)
            dyn_load.click()
            print("ran dynamic")
            sleep(5)
            i -= 1
        except:
            print("Finished Load more")
            break

# call function
load_more()

soup = BeautifulSoup(driver.page_source, 'lxml')

# begin scraping data once function completes

# depart times
dep_times = soup.find_all('span', attrs={'class': 'depart-time base-time'})
departure_time = []
for div in dep_times:
    departure_time.append(div.getText()[:-1])

# Arrival times
arr_times = soup.find_all('span', attrs={'class': 'arrival-time base-time'})
arrival_time = []
for div in arr_times:
    arrival_time.append(div.getText()[:-1])

# airline
airlines = soup.find_all('div', attrs={'dir': "ltr"})
airline = []
for div in airlines:
    airline.append(div.getText().strip("\n")[:-1])

# layovers
# needs regex here since different for additional stops
regex_stops = re.compile('.*stops-text*.')
stops = soup.find_all('span', attrs={'class': regex_stops})
layover = []
for div in stops:
    layover.append(div.getText().strip("\n")[:-1])

# price
regex_price = re.compile(".*-mb-aE-*.")
prices = soup.find_all('span', attrs={'id': regex_price})
price = []
for div in prices:
    price.append(div.getText().strip("\n")[:-1])

# am or pr
meridies = soup.find_all('span', attrs={'class': 'time-meridiem meridiem'})
meridiem = []
for div in meridies:
    meridiem.append(div.getText())

# format data such as splitting and matching flight times and dates.

airline = np.asarray(airline)
airline = airline.reshape(int(len(airline) / 2), 2)

layover = np.asarray(layover)
layover = layover.reshape(int(len(layover) / 2), 2)

departure_time = np.asarray(departure_time)
departure_time = departure_time.reshape(int(len(departure_time) / 2), 2)

arrival_time = np.asarray(arrival_time)
arrival_time = arrival_time.reshape(int(len(arrival_time) / 2), 2)

meridiem = np.asarray(meridiem)
meridiem = meridiem.reshape(int(len(meridiem) / 4), 4)

# set max_columns to see full size
pd.set_option('display.max_columns', None)


# using pandas to construct dataframe.
# loops over certain data inorder to line up flight information.
df = pd.DataFrame({"origin": departure,
                   "destination": arrival,
                   "layovers_o": [m for m in layover[:, 0]],
                   "layovers_d": [m for m in layover[:, 1]],
                   "airline_o": [m for m in airline[:, 0]],
                   "airline_d": [m for m in airline[:, 1]],
                   "startdate": departure_date,
                   "enddate": arrival_date,
                   "price": price,
                   "currency": "USD",
                   "deptime_o": [m + str(n) for m, n in zip(departure_time[:, 0], meridiem[:, 0])],
                   "arrtime_d": [m + str(n) for m, n in zip(arrival_time[:, 0], meridiem[:, 1])],
                   "deptime_d": [m + str(n) for m, n in zip(departure_time[:, 1], meridiem[:, 2])],
                   "arrtime_o": [m + str(n) for m, n in zip(arrival_time[:, 1], meridiem[:, 3])]
                   })

print(df.head())
