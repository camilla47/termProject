
import re
import numpy as np
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
import re

def bsoup_scrape_data(titles, years, episodes, countries, scores, ranks, soup):
    # SHOW TITLES
    show_titles = soup.find_all('h6', class_='text-primary')
    for title in show_titles:
        title = title.text.strip()
        titles.append(title)

    # COUNTRY / YEAR / EPISODES
    show_info = soup.find_all('span', class_='text-muted')
    for info in show_info:
        # get the info
        info = info.text.strip()

        # extract the year
        year = info.split(',')[0][-4:]
        year = int(year)
        years.append(year)

        # extract the episode
        episode = info.split(',')[1]
        numbers = re.findall(r'\d+', episode)
        ep_length= int(numbers[0])
        episodes.append(ep_length)
        country = info.split(' ')[0] 
        countries.append(country)

    # SHOW SCORES
    show_scores = soup.find_all('span', class_='score')
    for score in show_scores:
        score = score.text.strip()
        scores.append(score)

    # SHOW RANKS
    show_rank = soup.find_all('div', class_='ranking pull-right')
    for rank in show_rank:
        rank = rank.text.strip()
        rank = int(rank.split("#")[1])
        ranks.append(rank)


years = []
episodes = []
countries = []
titles = []
scores = []
ranks = []
genres = []
networks = []
watchers = []

# URL to scrape
url = 'https://mydramalist.com/shows/top?page=1'
# Send a GET request to the URL
response = requests.get(url)
# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
bsoup_scrape_data(titles, years, episodes, countries, scores, ranks, soup)

my_drama_list_dummy = pd.DataFrame({
    "title": titles,
    "year": years,
    "episodes": episodes,
    "viewer_score": scores,
    "rank": ranks
})

mdl = pd.DataFrame(my_drama_list_dummy)
print("thee ned")
mdl.to_csv("dummy.csv", index=False)
