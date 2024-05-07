from models.offer import Offer
from .offfer_scraper import OfferScraper
import requests
from bs4 import BeautifulSoup
from typing import List
from typing import Tuple
import re
import sys
import html

class OfferScraperPracuj(OfferScraper):
    __SOURCE = 'it.pracuj.pl'

    def __init__(self, url):
        super().__init__(url) 

    def get_offers(self) -> List[Offer]:
        try:
            super().check_if_scraping_is_possible(self._url_to_scrap)
            response = requests.get(self._url_to_scrap, headers=self._headers)
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')

            section_offers_div = soup.find('div', {'data-test': 'section-offers'})

            if section_offers_div:
                links = section_offers_div.find_all('a', {'data-test': 'link-offer'})

                all_offers = []

                for link in links:
                    href_offer = link.get('href')

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

            job_offer_id = OfferScraperPracuj.__extract_offer_id_from_offer_url(offer_url)

            job_source = self.__SOURCE
            job_offer_url = offer_url

            job_position = soup.find('h1', {'data-test': 'text-positionName'}).text.strip()
            job_company = ''.join(soup.find('h2', {'data-test': 'text-employerName'}).find_all(text=True, recursive=False)).strip()
            job_category = soup.find('div', class_='v1xz4nnx').text.strip()

            job_min_salary, job_max_salary, job_salary_currency = OfferScraperPracuj.get_offer_sallary_info(soup)
            job_skills = OfferScraperPracuj.__get_skills(soup, job_offer_url)
            job_seniority = OfferScraperPracuj.__get_seniority(soup, job_offer_url)

            offer = Offer(job_offer_id, job_source, job_offer_url)
            offer.set_job_basic_info(job_category, job_position, job_company, job_seniority)
            offer.set_salary(job_min_salary, job_max_salary, job_salary_currency)
            offer.set_skills(job_skills)

            return offer
        except Exception as e:
            print(f"An error occurred while getting offer from {offer_url}: {e}")
            return None
    
    @staticmethod
    def __extract_offer_id_from_offer_url(url):
        pattern = r'oferta,(\d+)' 
        match = re.search(pattern, url)

        if match:
            offer_id = match.group(1)
            return offer_id
        
        return None
    
    @staticmethod
    def __get_salary_details(html_section_to_parse) -> Tuple[float, float, str]:
        salary_text = html_section_to_parse.find('div', {'data-test': 'text-earningAmount'}).text

        if "–" in salary_text:
            min_salary, max_salary = salary_text.split("–")
            min_salary = min_salary.replace(" ", "")
            max_salary = max_salary.replace(" ", "")
        else:
            min_salary = max_salary = salary_text.replace(" ", "")

        min_salary, max_salary = salary_text.split("–")
        min_salary = min_salary.replace(" ", "")
        max_salary = max_salary.replace(" ", "")

        salary_amount_unit = html_section_to_parse.find('div', class_='sxxv7b6').text
        currency = OfferScraper.get_currency(html.unescape(max_salary))

        min_salary_value = OfferScraper.convert_string_to_float_number(min_salary) if min_salary and max_salary else OfferScraper.convert_string_to_float_number(max_salary)
        max_salary_value = OfferScraper.convert_string_to_float_number(max_salary)

        min_salary_value = OfferScraper.get_final_salary(min_salary_value, salary_amount_unit)
        max_salary_value = OfferScraper.get_final_salary(max_salary_value, salary_amount_unit)

        return min_salary_value, max_salary_value, currency
    
    @staticmethod
    def __get_skills(html_section_to_parse, job_offer_url) -> List[str]:
        skills_section = html_section_to_parse.find('section', {'data-test': 'section-technologies-expected'})
        skills = []

        if skills_section:
            skills_tags = skills_section.find_all('p', class_='n1bzavn5')
            for skill_tag in skills_tags:
                skills.append(skill_tag.text)
        else:
            print(f"Skills could not be found for offer {job_offer_url}")

        return skills
    
    @staticmethod
    def get_offer_sallary_info(soup: BeautifulSoup) -> Tuple[float, float, str]:
        salaries_per_contract_type = soup.findAll('div', {'data-test': 'section-salaryPerContractType'})

        # this means that we have more than one contract type like B2B contract and contract of employement
        if(len(salaries_per_contract_type) > 0):
            min_salary_value = sys.maxsize
            max_salary_value = -sys.maxsize
            currency = None

            for salary_per_contract_section in salaries_per_contract_type:
                currently_min_salary_value, currently_max_salary_value, currency = OfferScraperPracuj.__get_salary_details(salary_per_contract_section)

                if(currently_min_salary_value < min_salary_value):
                    min_salary_value = currently_min_salary_value

                if(currently_max_salary_value > max_salary_value):
                    max_salary_value = currently_max_salary_value

            return min_salary_value, max_salary_value, currency
       
        return OfferScraperPracuj.__get_salary_details(soup)
    
    @staticmethod
    def __get_seniority(html_to_parse, offer_url) -> str:
        li_seniority_section = html_to_parse.find('li', {'data-test': 'sections-benefit-employment-type-name'})
        seniority_levels_tag = li_seniority_section.find('div', class_='t1g3wgsd')

        if seniority_levels_tag:
           return OfferScraper.get_max_seniority(seniority_levels_tag.text)
        else:
            print(f"Could not find seniority for offer {offer_url}")

        return None
    
