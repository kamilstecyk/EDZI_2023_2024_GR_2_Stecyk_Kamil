# -*- coding: utf-8 -*-
from scrapers.offer_scraper_pracuj import OfferScraperPracuj
from scrapers.offer_scraper_justjoinit import OfferScraperJustJoinIt
import json
import os

def write_data_to_json(filename, data):
    try:
        # Check if the "data" folder exists, if not, create it
        if not os.path.exists('data'):
            os.makedirs('data')

        # Construct the file path by joining the "data" folder path with the filename
        file_path = os.path.join('data', filename)

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Offers has been written successfully to json file {file_path}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def main():
    print('Script has started...')

    url_to_scrap_pracuj = 'https://it.pracuj.pl/praca/krakow;wp?rd=0&et=17%2C4%2C18&sal=1&sc=0&its=big-data-science&iwhpl=false'
    url_to_scrap_just_join_it = 'https://justjoin.it/krakow/data/experience-level_junior.mid.senior/salary_1.100000/with-salary_yes?orderBy=DESC&sortBy=newest'

    scrapers = [OfferScraperPracuj(url_to_scrap_pracuj), OfferScraperJustJoinIt(url_to_scrap_just_join_it)]

    merged_offers = []

    for scraper in scrapers:
        offers = scraper.get_offers()
        offers_dicts = [offer.to_dict() for offer in offers]

        for offer in offers_dicts:
            merged_offers.append(offer)

    json_file = 'offers-results.json'
    write_data_to_json(json_file, merged_offers)

    print("Scraping has finished.")

if __name__ == "__main__":
    main()