import requests
from bs4 import BeautifulSoup 
import pandas as pd
from datetime import date
import plotly.express as px

def get_dynamic_url(base_url='https://github.com/trending',language="python",date_range="weekly"):
    scrape_url = f"https://github.com/trending/{language}?since={date_range}&spoken_language_code=en"
    return scrape_url

def get_data_as_soup(url):
    page = requests.get(url)
    if page.status_code == 200:
        return BeautifulSoup(page.text, 'html5lib')

def view_raw_data(soup):
    return soup
    
def get_rows(soup):
    rows = []
    tag = 'article'
    tagclass = "Box-row"
    rows = soup.find_all(tag,attrs={'class':tagclass})
    return rows

def extract_data(rows,date):
    datadict = []
    for item in rows :
        username, reponame = item.find('h1').text.replace(' ','').split()

        try:description = item.find('p').text 
        except: description = ""

        link = "https://github.com/" + item.find('h1').find('a').attrs.get('href')
        language = item.find('span',attrs={'itemprop':'programmingLanguage'}).text
        starsTag,forkTag = item.find_all('a',attrs={'class':'muted-link'})
        stars = starsTag.text
        forks = forkTag.text
        datadict.append({
            'username': username,
            'repository':reponame,
            'link' : link,
            'total_stars':stars,
            'total_forks':forks,
            'language':language,
            'range':date,
            'description':description
        })
    return datadict

def save_data(datadict,lang,range):
    df = pd.DataFrame(datadict)
    df.to_csv('datasets/'+lang+'_'+range+'_'+str(date.today()),index=False)
    return df

def generate_graph(filepath):
    df = pd.read_csv(filepath)
    df.total_stars = df.total_stars.apply(lambda val :int(val.strip().replace(',','')))
    df.total_forks = df.total_forks.apply(lambda val :int(val.strip().replace(',','')))
    fig = px.bar(df,x='repository',y='total_stars',title=filepath,color='total_forks')
    # fig = px.bar(df,x='repository',y='total_stars',title=filepath)
    return fig