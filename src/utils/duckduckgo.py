import requests
from bs4 import BeautifulSoup

def make_request(search_term):
    search_term = search_term.replace(' ', '+')
    url = f"https://duckduckgo.com/html/?q={search_term}"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    return response.text

def duckduckgo(search_term):
    response = make_request(search_term)

    soup = BeautifulSoup(response, 'html.parser')

    search_results = soup.select('#links.results .result__url')
    urls = [result['href'] for result in search_results]

    search_result_titles = soup.select('#links.results .result__title')
    titles = [title.get_text(strip=True) for title in search_result_titles]

    return list(zip(titles, urls))[0:8]