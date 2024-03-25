import ssl
import requests
from bs4 import BeautifulSoup
import urllib.robotparser
import re
import urllib.parse
import json

# refactor code

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en-US,en;q=0.9'}
class Movie:
    def __init__(self, ranking, title, rating):
        self.ranking = ranking
        self.title = title
        self.rating = rating
    
    def __str__(self):
        return f"{self.ranking}. {self.title}, rating: {self.rating}"

def create_movie_json_object(movie1, movie2):
    final_result = {
        "tytul_filmu": movie1.title,
        "ranking_imdb": movie1.ranking,
        "ocena_imdb": movie1.rating,
        "ocena_rotten_tomatoes": movie2.rating 
    }   

    return final_result

def check_if_scraping_is_possible(url):
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.scheme + "://" + parsed_url.netloc

    rp = urllib.robotparser.RobotFileParser() 
    rp.set_url(f"{domain}/robots.txt")
    rp.read()

    if rp.can_fetch("MyBot", url):
        print(f"Scraping is allowed for URL: {url}") 
    else:
        print(f"Scraping is not allowed for this URL: {url} according to robots.txt")
        
def get_movie_from_2_filmdb(search_url, movie_title):
    encoded_title = urllib.parse.quote(movie_title)
    response = requests.get(search_url + encoded_title, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_part = soup.find('search-page-result', type='movie')

    if movie_part is None:
        print("No movie matches for: ", movie_title)
        return
    
    movies = movie_part.select('search-page-media-row')

    rate = None

    for movie in movies:
        title = movie.find('a', slot='title')

        if title.text.strip() == movie_title.strip() and 'tomatometerscore' in movie.attrs:
            rate = movie['tomatometerscore']
            # print(title.text.strip(), " ", rate.strip())
            return Movie(None, title.text.strip().encode('utf-8').decode('unicode_escape'), rate.strip())

    return None

def get_movies_from_1_filmdb(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies_list = soup.find('ul', class_='ipc-metadata-list')

    found_movies = []

    if movies_list:
        li_movies = movies_list.find_all('li', class_='ipc-metadata-list-summary-item')
        for movie in li_movies:
            imdb_rating = movie.find('span', class_='ipc-rating-star--imdb')
            cleaned_rating = imdb_rating.text.split('(')[0].strip()

            movie_title = movie.select_one('a.ipc-title-link-wrapper h3')
            match = re.match(r'^(\d+\.)\s*(.*)$', movie_title.text)
            cleaned_movie_title = match.group(2).encode('utf-8').decode('unicode_escape')
            cleaned_movie_ranking = match.group(1)[:-1]

            # print(movie_title_cleaned, " ", cleaned_imdb_rating)
            found_movies.append(Movie(cleaned_movie_ranking, cleaned_movie_title, cleaned_rating))
    
    return found_movies
    
print("Web scraping has been started")

first_movie_db_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250&sort=rank%2Casc'
second_movie_db_url = 'https://www.rottentomatoes.com/search?search='

check_if_scraping_is_possible(first_movie_db_url)
check_if_scraping_is_possible(second_movie_db_url)

movies = get_movies_from_1_filmdb(first_movie_db_url)

results_data = []

movie_result_counter = 0
for movie_1 in movies:
    movie_2 =  get_movie_from_2_filmdb(second_movie_db_url, movie_1.title)
    if movie_2 is None or movie_2.rating == "":
        continue
    else:
        results_data.append(create_movie_json_object(movie_1, movie_2))
        movie_result_counter += 1
        print("Added successfully record for movie: ", movie_1.title)
    
    if movie_result_counter >= 10:
        break

file_path = "final_results.json"

with open(file_path, 'w') as json_file:
        json.dump(results_data, json_file, indent=4)
    
