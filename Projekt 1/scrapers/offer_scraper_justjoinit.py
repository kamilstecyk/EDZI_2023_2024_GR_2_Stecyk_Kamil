import sys
from typing import List, Tuple

from bs4 import BeautifulSoup
import requests

from models.offer import Offer
from .offfer_scraper import OfferScraper

class OfferScraperJustJoinIt(OfferScraper):
    __SOURCE = 'justjoin.it'

    def __init__(self, url):
        super().__init__(url) 

    def get_offers(self) -> List[Offer]:
        try:
            super().check_if_scraping_is_possible(self._url_to_scrap)
            response = requests.get(self._url_to_scrap, headers=self._headers)
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')

            section_offers_div = soup.find('div', {'data-test-id': 'virtuoso-item-list'})

            if section_offers_div:
                links = section_offers_div.find_all('a', class_="offer_list_offer_link")

                all_offers = []

                for link in links:
                    href_offer = 'https://' + self.__SOURCE + link.get('href')
                    offer = self.get_offer(href_offer)

                    if offer:
                        all_offers.append(offer)
                        print(offer.url)

                print("Number of offers: ", len(all_offers))
                return all_offers
            else:
                print('Cannot find offers!')
                return []
        except Exception as e:
            print(f"An error occurred while getting offers from {self._url_to_scrap}: {e}")
            return []
        
    def get_offer(self, offer_url) -> Offer:
        try:
            response = requests.get(offer_url, headers=self._headers)
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')

            job_offer_id = None
            job_source = self.__SOURCE
            job_offer_url = offer_url

            job_position = soup.find('h1', class_="css-1u65tlp").text
            job_company = soup.find('div', class_="css-mbkv7r").text
            job_category = soup.find('div', class_="css-6t6cyr").text
            job_seniority = soup.find_all('div', class_="css-15wyzmd")[1].text

            job_min_salary, job_max_salary, job_salary_currency = OfferScraperJustJoinIt.__get_salary_details(soup)
            job_skills = OfferScraperJustJoinIt.__get_skills(soup, job_offer_url)

            offer = Offer(job_offer_id, job_source, job_offer_url)
            offer.set_job_basic_info(job_category, job_position, job_company, job_seniority)
            offer.set_salary(job_min_salary, job_max_salary, job_salary_currency)
            offer.set_skills(job_skills)
            
            return offer
        except Exception as e:
            print(f"An error occurred while getting offer from {offer_url}: {e}")
            return None
    
    @staticmethod
    def __get_skills(soup, offer_url) -> List[str]:
        skills_section = soup.find('ul', class_="css-1uak81x")

        all_skills = []

        if(skills_section):
            skills_tags = skills_section.find_all('h6', class_="css-x1xnx3")

            for skill_tag in skills_tags:
                all_skills.append(skill_tag.text)
        else:
            print(f"Could not find skills for {offer_url}")

        return all_skills
    
    @staticmethod
    def __get_salary_details(html_section_to_parse) -> Tuple[float, float, str]:
        salaries_per_contract_type = html_section_to_parse.find_all('div', class_="css-1d9s327")
        
        min_salary_value = sys.maxsize
        max_salary_value = -sys.maxsize
        currency = None

        for salary_per_contract in salaries_per_contract_type:
            salary_amount_unit = salary_per_contract.find('span', class_="css-1waow8k").text

            salary_tag = salary_per_contract.find('span', class_="css-1pavfqb")
            salary_range = salary_tag.text.split('-')

            current_currency = OfferScraper.get_currency(salary_tag.text)
            currently_min_salary = OfferScraper.convert_string_to_float_number(salary_range[0])
            currently_max_salary = OfferScraper.convert_string_to_float_number(salary_range[1]) if len(salary_range) > 1 else OfferScraper.convert_string_to_float_number(salary_range[0])

            currently_min_salary = OfferScraper.get_final_salary(currently_min_salary, salary_amount_unit)
            currently_max_salary = OfferScraper.get_final_salary(currently_max_salary, salary_amount_unit)
            currency = current_currency

            if(currently_min_salary < min_salary_value):
                min_salary_value = currently_min_salary

            if(currently_max_salary > max_salary_value):
                max_salary_value = currently_max_salary

        return min_salary_value, max_salary_value, currency