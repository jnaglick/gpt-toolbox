from bs4 import BeautifulSoup
import re
import requests

def make_request(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    return response.text

def web_request(url):
        response = make_request(url)
        soup = BeautifulSoup(response, 'html.parser')
        soup_text = soup.get_text()
        result = re.compile(r'\W+').sub(' ', soup_text)
        result = ' '.join(result.split(' '))
        return result

# print(web_request("https://www.mlb.com/mets/schedule/2023-04"))
