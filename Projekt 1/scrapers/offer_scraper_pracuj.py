from models.offer import Offer
from .offfer_scraper import OfferScraper
import requests
from bs4 import BeautifulSoup
from typing import List
from typing import Tuple
import re
import sys

class OfferScraperPracuj(OfferScraper):
    SOURCE = 'it.pracuj.pl'

    def __init__(self, url):
        super().__init__(url) 

    def get_offers(self) -> List[Offer]:
        try:
            super().check_if_scraping_is_possible(self.url_to_scrap)
            response = requests.get(self.url_to_scrap, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')

            section_offers_div = soup.find('div', {'data-test': 'section-offers'})

            if section_offers_div:
                links = section_offers_div.find_all('a', {'data-test': 'link-offer'})

                for link in links:
                    href_offer = link.get('href')

                    offer = self.__get_offer(href_offer)

                return []
            else:
                print('Cannot find offers!')
                return []
        except Exception as e:
            print(f"An error occurred while getting offers from {self.url_to_scrap}: {e}")
            return []

        return []
    
    def __get_offer(self, offer_url) -> Offer:
        try:
            response = requests.get(offer_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')

            job_offer_id = OfferScraperPracuj.extract_offer_id_from_offer_url(offer_url)
            job_source = self.SOURCE
            job_offer_url = offer_url
            job_position = soup.find('h1', {'data-test': 'text-positionName'}).text
            job_company = soup.find('h2', {'data-test': 'text-employerName'}).text

            job_min_salary, job_max_salary, job_salary_currency = OfferScraperPracuj.get_offer_sallary_info(soup)

            skills = None
            job_category = soup.find('span', class_='offer-viewPFKc0t').text
            job_seniority = None

            print(job_offer_id)
            print(job_source)
            print(job_offer_url)
            print(job_position)
            print(job_company)
            print(job_min_salary)
            print(job_max_salary)
            print(job_salary_currency)
            print(job_category)
            print("\n")

            
        except Exception as e:
            print(f"An error occurred while getting offer from {offer_url}: {e}")
            return None

        return None
    
    @staticmethod
    def extract_offer_id_from_offer_url(url):
        pattern = r'oferta,(\d+)' 
        match = re.search(pattern, url)

        if match:
            offer_id = match.group(1)
            return offer_id
        
        return None
    
    @staticmethod
    def get_offer_sallary_info(soup: BeautifulSoup) -> Tuple[float, float, str]:
        salaries_per_contract_type = soup.findAll('div', {'data-test': 'section-salaryPerContractType'})

        # this means that we have more than one contract type like B2B contract and contract of employement
        if(len(salaries_per_contract_type) > 0):
            min_salary_value = sys.maxsize
            max_salary_value = -sys.maxsize
            currency = None

            for salary_per_contract_section in salaries_per_contract_type:
                currently_min_salary_value, currently_max_salary_value, currency = OfferScraperPracuj.get_salary_details(salary_per_contract_section)

                if(currently_min_salary_value < min_salary_value):
                    min_salary_value = currently_min_salary_value

                if(currently_max_salary_value > max_salary_value):
                    max_salary_value = currently_max_salary_value

            return min_salary_value, max_salary_value, currency
       
        return OfferScraperPracuj.get_salary_details(soup)


    @staticmethod
    def convert_string_to_float_number(dirty_number: str) -> float:
        cleaned_number = re.sub(r'[^\d,.]', '', dirty_number)
        cleaned_float_number = float(cleaned_number.replace(',', '.'))
        return cleaned_float_number

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
    def get_final_salary(salary: str, salary_amount_unit: str) -> float:
        if('hr.' in salary_amount_unit or 'godz.' in salary_amount_unit):
                salary *= 168
           
        if('net' in salary_amount_unit):
                salary *= 1.23
        
        return salary
    
    @staticmethod
    def get_salary_details(html_section_to_parse) -> Tuple[float, float, str]:
        min_salary = html_section_to_parse.find('span', {'data-test': 'text-earningAmountValueFrom'})
        max_salary = html_section_to_parse.find('span', {'data-test': 'text-earningAmountValueTo'})

        salary_amount_unit = html_section_to_parse.find('span', {'data-test': 'text-earningAmountUnit'}).text
        currency = OfferScraperPracuj.get_currency(max_salary.text)

        min_salary_value = OfferScraperPracuj.convert_string_to_float_number(min_salary.text) if min_salary and max_salary else OfferScraperPracuj.convert_string_to_float_number(max_salary.text)
        max_salary_value = OfferScraperPracuj.convert_string_to_float_number(max_salary.text)

        min_salary_value = OfferScraperPracuj.get_final_salary(min_salary_value, salary_amount_unit)
        max_salary_value = OfferScraperPracuj.get_final_salary(max_salary_value, salary_amount_unit)

        return min_salary_value, max_salary_value, currency
