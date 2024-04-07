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
    print('Script has started...')

    url_to_scrap_pracuj = 'https://it.pracuj.pl/praca/krakow;wp?rd=0&et=17%2C4%2C18&sal=1&sc=0&its=big-data-science&iwhpl=false'
    pracuj_scraper = OfferScraperPracuj(url_to_scrap_pracuj)
    offers = pracuj_scraper.get_offers()

    offers_dicts = [offer.to_dict() for offer in offers]
    json_file_path = 'pracujpl-results.json'
    write_data_to_json(json_file_path, offers_dicts)
    print(f"Offers has been written to json file {json_file_path}")

    print("Scraping has finished.")

if __name__ == "__main__":
    main()