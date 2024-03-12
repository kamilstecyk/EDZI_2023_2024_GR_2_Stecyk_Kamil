import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    absolutes = [urljoin(url, link['href']) for link in links]
    return absolutes

url = 'https://www.onet.pl/'
links = get_links(url)

current_link = links[random.randint(0, len(links) - 1)]
print(current_link)

for i in range(0, 99):
    links = get_links(current_link)
    current_link = links[random.randint(0, len(links) - 1)]
    print(current_link)

