import pandas as pd
from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
from IPython.core.display import clear_output
from warnings import warn  # show us warning if the status code is not 200

headers = {"Accept-Language": "en-US, en;q=0.5"}

urls = []
names = []
ratings = []
years = []
metascores = []
votes = []
start_indexes = []
release_years = [str(i) for i in range(2009, 2019)]
# print(release_years)

for i in range(1, 5):  # top 4 pages only for each year
    start_indexes.append(str(50*(i-1)+1))
# print(start_indexes)

for release_year in release_years:
    for start_index in start_indexes:
        url = 'https://www.imdb.com/search/title/?release_date=' + release_year + '&sort=num_votes,desc&start=' + start_index + '&ref_=adv_nxt'
        # print(url)
        urls.append(url)
# print(urls)

for url in urls:
    data = requests.get(url, headers)
    if data.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, data.status_code))

    sleep(randint(8, 15))
    # print(data.text)
    soup = BeautifulSoup(data.text, 'html.parser')
    movie_container = soup.find_all('div', class_='lister-item mode-advanced')
    # print(len(movie_container))
    for movie in movie_container:
        # print(movie)
        sleep(randint(1, 5))
        # print('movie_container')
        if movie.find('span', class_='metascore') is not None:
            # print('movie')
            movie_name = movie.find('div', class_='lister-item-content')
            # print(movie_name)
            names.append(movie_name.h3.a.text)
            # print(movie_name.strong.text)
            ratings.append(str(movie_name.strong.text))
            year = movie_name.h3.find('span', class_='lister-item-year text-muted unbold').text
            # print(year)
            years.append(year)
            metascore = movie_name.find('div', class_='ratings-bar')
            metascore = metascore.find('div', class_='inline-block ratings-metascore')
            # print(metascore.span.text)
            metascores.append(str(metascore.span.text))
            vote = movie_name.find('span', attrs={'name':'nv'})['data-value']
            # print(int(vote))
            votes.append(vote)
    clear_output(wait=True)  # send request once the respond has received. wait before sending another request


table_df = pd.DataFrame({'movie': names,
'year': years,
'imdb': ratings,
'metascore': metascores,
'votes': votes
})
table_df.loc[:, 'year'] = table_df['year'].str[-5:-1].astype(int)
table_df.to_csv('imdb_ratings.csv')
print("Done!")

