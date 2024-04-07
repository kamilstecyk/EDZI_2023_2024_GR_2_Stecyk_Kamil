# -*- coding: utf-8 -*-
from scrapers.offer_scraper_pracuj import OfferScraperPracuj
import json

def write_data_to_json(file_path, data):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        print(f"Error writing to file: {e}")

def main():
    print('Script is executing...')

    url_to_scrap_pracuj = 'https://it.pracuj.pl/praca/krakow;wp?rd=0&et=17%2C4%2C18&sal=1&sc=0&its=big-data-science&iwhpl=false'
    pracuj_scraper = OfferScraperPracuj(url_to_scrap_pracuj)
    pracuj_scraper.get_offers()


if __name__ == "__main__":
    main()