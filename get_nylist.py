
# This scripts aims to get all book names on historic New York Time Best Sellers (Business section)
# The purpose is to:
#   1. help to compile my reading list in 2020
#   2. serve as reference to use Python for simple web analytics

# One interesting finding:
#   1. no best seller list for 2015-08, maybe a bug in New York Times system

import requests
import pandas as pd
from bs4 import BeautifulSoup

nylist = pd.DataFrame()

# the earliest list is 2013/11/01, so the starting year is 2013
for the_year in range(2013, 2020):
    for the_month in range(1, 13):

        # one need to get the URL pattern first, and then use Requests package to get the URL content
        url = 'https://www.nytimes.com/books/best-sellers/{0}/{1}/01/business-books/'.format(the_year, str(the_month).zfill(2))
        page = requests.get(url)
        print(" --  try: {0}, {1} -- ".format(the_year, str(the_month).zfill(2)))

        # ensure proper result is returned
        if page.status_code != 200:
            continue

        # one may want to use BeautifulSoup to parse the right elements out
        soup = BeautifulSoup(page.text, 'html.parser')
        # the specific class names are unique for this URL and they don't change across all URLs
        top_list = soup.findAll("ol", {"class": "css-12yzwg4"})[0].findAll("div", {"class": "css-xe4cfy"})
        print(the_year, the_month, len(top_list))

        # loop through the Best Seller list in each Year-Month, and append the information into a pandas DataFrame
        for i in range(len(top_list)):
            book = top_list[i].contents[0]
            title = book.findAll("h3", {"class": "css-5pe77f"})[0].text
            author = book.findAll("p", {"class": "css-hjukut"})[0].text
            review = book.get("href")
            # print("{0}, {1}; review: {2}".format(title, author, review))
            one_item = pd.Series([the_year, the_month, title, author, i+1, review], index=['year', 'month', 'title', 'author', 'rank', 'review'])
            nylist = nylist.append(one_item, ignore_index=True, sort=False)

# write out the result to a pickle file for easy analysis later.
nylist.to_pickle("nylist.pkl")
nylist.to_csv("nylist.csv", index=False)