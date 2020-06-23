import requests
from bs4 import BeautifulSoup 
import pandas as pd

def get_dynamic_url(base_url='https://github.com/trending',language="python",date_range="weekly"):
    scrape_url = f"https://github.com/trending/{language}?since={date_range}&spoken_language_code=en"
    return scrape_url

def get_data_as_soup(url):
    page = requests.get(url)
    if page.status_code == 200:
        return BeautifulSoup(page.text, 'html5lib')

def view_raw_data(soup):
    return soup
    