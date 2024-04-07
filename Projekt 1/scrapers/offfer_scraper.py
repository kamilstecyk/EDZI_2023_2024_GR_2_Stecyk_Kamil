from models import offer 
from typing import List
import urllib.parse
import urllib.robotparser

class OfferScraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en-US,en;q=0.9'}

    url_to_scrap = None

    def __init__(self, url):
        self.url_to_scrap = url

    @staticmethod
    def check_if_scraping_is_possible(url):
        try: 
            parsed_url = urllib.parse.urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{domain}/robots.txt")
            rp.read()

            if rp.can_fetch(OfferScraper.headers['User-Agent'], url):
                print(f"Scraping is allowed for URL: {url}")
            else:
                print(f"Scraping is not allowed for this URL: {url} according to robots.txt")
        except Exception as e:
            print(f"An error occurred while checking if scraping is possible for URL {url}: {e}")

    def get_offers(self) -> List[offer.Offer]:
        pass

    def __get_offer(self, offer_url) -> offer.Offer:
        pass
