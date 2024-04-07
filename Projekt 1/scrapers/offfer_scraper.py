from models import offer 
from typing import List
import urllib.parse
import urllib.robotparser
import re

class OfferScraper():
    _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en-US,en;q=0.9'}

    _url_to_scrap = None

    def __init__(self, url):
        self._url_to_scrap = url

    @staticmethod
    def check_if_scraping_is_possible(url):
        try: 
            parsed_url = urllib.parse.urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{domain}/robots.txt")
            rp.read()

            if rp.can_fetch(OfferScraper._headers['User-Agent'], url):
                print(f"Scraping is allowed for URL: {url}")
            else:
                print(f"Scraping is not allowed for this URL: {url} according to robots.txt")
        except Exception as e:
            print(f"An error occurred while checking if scraping is possible for URL {url}: {e}")

    #TODO fix bug
    # there is a problem with coding 
    @staticmethod
    def get_currency(price: str) -> str:
        currency_match = re.search(r'([A-Za-zł$€]+)', price)

        if currency_match:
            currency = currency_match.group(1)
            return currency
       
        return None
    
    @staticmethod
    def convert_string_to_float_number(dirty_number: str) -> float:
        cleaned_number = re.sub(r'[^\d,.]', '', dirty_number)
        cleaned_float_number = float(cleaned_number.replace(',', '.'))
        return cleaned_float_number
    
     # given_seniority_levels is a string with seniority levels
    @staticmethod
    def get_max_seniority(given_seniority_levels: str) -> str:
        seniority_levels = ['junior', 'regular', 'mid', 'senior']
        pattern = re.compile(r'\b(?:senior|mid|regular|junior)\b', re.IGNORECASE | re.MULTILINE)

        levels_found = pattern.findall(given_seniority_levels)
        max_seniority_level = None

        for level in levels_found:
            index = seniority_levels.index(level.strip().lower())
            
            if max_seniority_level is None or index > seniority_levels.index(max_seniority_level):
                max_seniority_level = level.strip().lower()

        return max_seniority_level

    def get_offers(self) -> List[offer.Offer]:
        pass

    def __get_offer(self, offer_url) -> offer.Offer:
        pass
