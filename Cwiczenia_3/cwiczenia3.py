from typing import List
import urllib.parse
import urllib.robotparser
import requests
from bs4 import BeautifulSoup
import json
import re

class Movie:
    def __init__(self, ranking, title, rating):
        self.ranking = ranking
        self.title = title
        self.rating = rating

class MovieJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Movie):
            return obj.__dict__
        return super().default(obj)

class WebScraper:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en-US,en;q=0.9'}

    def __init__(self, imdb_url, rt_url):
        self.imdb_url = imdb_url
        self.rt_url = rt_url

    @staticmethod
    def check_if_scraping_is_possible(url):
        try: 
            parsed_url = urllib.parse.urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{domain}/robots.txt")
            rp.read()

            if rp.can_fetch(WebScraper.headers['User-Agent'], url):
                print(f"Scraping is allowed for URL: {url}")
            else:
                print(f"Scraping is not allowed for this URL: {url} according to robots.txt")
        except Exception as e:
            print(f"An error occurred while checking if scraping is possible for URL {url}: {e}")

    def get_movies_from_imdb(self) -> List[Movie]:
        try:
            response = requests.get(self.imdb_url, headers=WebScraper.headers)
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
                    cleaned_movie_title = match.group(2)
                    cleaned_movie_ranking = match.group(1)[:-1]
                    found_movies.append(Movie(cleaned_movie_ranking, cleaned_movie_title, cleaned_rating))
            return found_movies
        except Exception as e:
            print(f"An error occurred while getting movies from IMDb: {e}")
            return []

    def get_movie_from_rt(self, movie_title) -> Movie:
        try:
            encoded_title = urllib.parse.quote(movie_title)
            response = requests.get(f"{self.rt_url}{encoded_title}", headers=WebScraper.headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            movie_part = soup.find('search-page-result', type='movie')

            if movie_part is None:
                print("No movie matches for: ", movie_title)
                return None
            
            movies = movie_part.select('search-page-media-row')

            for movie in movies:
                title = movie.find('a', slot='title')
                if title.text.strip() == movie_title.strip() and 'tomatometerscore' in movie.attrs:
                    rate = movie['tomatometerscore']
                    return Movie(None, title.text.strip(), rate.strip())
            return None
        except Exception as e:
            print(f"An error occurred while getting movie from Rotten Tomatoes: {e}")
            return None

def create_movie_json_object(movie1, movie2):
    return {
        "title": movie1.title,
        "imdb_ranking": movie1.ranking,
        "imdb_rating": movie1.rating,
        "rt_rating": movie2.rating
    }

def main():
    print("Web scraping has been started")

    movies_db_imdb = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250&sort=rank%2Casc'
    search_movie_in_rt = 'https://www.rottentomatoes.com/search?search='

    scraper = WebScraper(movies_db_imdb, search_movie_in_rt)
    scraper.check_if_scraping_is_possible(movies_db_imdb)
    scraper.check_if_scraping_is_possible(search_movie_in_rt)
    
    movies = scraper.get_movies_from_imdb()

    results_data = []
    movie_result_counter = 0

    for movie_1 in movies:
        movie_2 = scraper.get_movie_from_rt(movie_1.title)

        if movie_2 is None or movie_2.rating == "":
            continue
        else:
            results_data.append(create_movie_json_object(movie_1, movie_2))
            movie_result_counter += 1
            print("Added successfully record for movie: ", movie_1.title)

        if movie_result_counter >= 100:
            break

    file_path = "final_results.json"

    try:
        with open(file_path, 'w') as json_file:
            json.dump(results_data, json_file, cls=MovieJSONEncoder, indent=4)
    except IOError as e:
        print(f"Error writing to file: {e}")
    
    print(f"Successfully added to json file {movie_result_counter} movies records")

if __name__ == "__main__":
    main()