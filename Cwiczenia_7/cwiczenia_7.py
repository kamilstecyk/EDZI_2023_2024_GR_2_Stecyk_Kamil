import requests 
from summarizer import Summarizer

def get_random_wikipedia_article_text():
    # Endpoint URL for the MediaWiki API
    endpoint = "https://en.wikipedia.org/w/api.php"

    article_params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": "Natural language processing",
        "explaintext": True  
    }
    article_response = requests.get(endpoint, params=article_params)
    if article_response.status_code == 200:
        article_data = article_response.json()
        # Extract the text of the article
        article_text = next(iter(article_data["query"]["pages"].values()))["extract"]
        return article_text
    else:
        print("Failed to fetch article text")

# Example usage:
random_article_text = get_random_wikipedia_article_text()
print(random_article_text)

summarizer = Summarizer()

summary = summarizer(random_article_text, min_length=150, max_length=500)

with open("org.txt", "w") as file:
    file.write(random_article_text)

with open('outcome.txt', 'w') as file:
    file.write(summary)