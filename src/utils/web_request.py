from bs4 import BeautifulSoup
import re
import requests

def make_request(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises stored HTTPError, if one occurred (?)
    return response.text

def web_request(url, apply_soup=True, remove_symbols=False, collapse_whitespace=True):
        try:
            response = make_request(url)
        except:
            return ""

        if apply_soup:
            response = BeautifulSoup(response, 'html.parser').get_text()
        
        if remove_symbols:
            response = re.compile(r'\W+').sub(' ', response)             

        if collapse_whitespace:
            response = ' '.join(response.split())

        return response
