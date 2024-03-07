import requests
from bs4 import BeautifulSoup
import re

def get_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # mw-parser-output to klasa HTML uzywana na platformie MediaWiki - jest glownym kontenerem dla tresci
    content = soup.find('div', class_='mw-parser-output').text
    return content

def process_text(text):
    #Dopisz kod spelniajacy Punkt 2
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.strip()
    return text

def get_ranked_words(text):
    ranked_words = {}
    #Dopisz kod spelniajacy Punkt 3
    words = text.split()

    for word in words: 
        cleaned_word = word.strip()

        if(cleaned_word in ranked_words):
            ranked_words[cleaned_word] += 1
        else:
            ranked_words[cleaned_word] = 1

    sliced_ranked_words = dict(list(ranked_words.items())[:100])
    ranked_words = dict(sorted(sliced_ranked_words.items(), key=lambda x: x[1], reverse=True))
    return ranked_words

def write_results(results, filename):
    with open(filename, 'w') as file:
    #Dopisz kod spelniajacy Punkt 4
        rank = 1
        for word, occurrences in results.items():
            file.write(f"{rank};{word};{occurrences}\n")
            rank += 1
        pass

def main():
    url = 'https://en.wikipedia.org/wiki/Web_scraping'
    text = get_text(url)
    cleaned_text = process_text(text)
    final_words = get_ranked_words(cleaned_text)
    write_results(final_words, 'output.txt')

if __name__ == "__main__":
    main()