# class = a-link-normal a-text-normal

import urllib.request
from bs4 import BeautifulSoup as bs
import io
import urllib.parse as urlparse
from urllib.parse import parse_qs

def scrape(address, agent):
    print('Using agent: {}'.format(agent))
    print('Scraping url: {}'.format(address))

    request = urllib.request.Request(
        address,
        headers={
            'User-Agent': agent
        }
    )

    page = urllib.request.urlopen(request)
    
    soup = bs(page.read(), 'html5lib')

    return getLinks(soup)


def validItem(url):
    parsed = urlparse.urlparse(url)
    qs = parse_qs(parsed.query)
    if 's' in qs and qs['s'] == ['merchant-items']:
        if '#customerReviews' not in url:
            return True
    return False
    

def getLinks(soup):
    links = []

    linkObjects = soup.find_all('a', href=True, attrs={'class': ['a-link-normal', 'a-text-normal']})

    baseUrl = 'https://www.amazon.es'

    for obj in linkObjects:
        formedUrl = '{}{}'.format(baseUrl, obj['href'])
        if validItem(formedUrl):
            links.append(formedUrl)
    
    links = list(set(links))
    
    return links


def getProductId(url):
    parsed = urlparse.urlparse(url)
    path = parsed.path
    prodId = ''
    try:
        pathSplits = path.split('/')
        prodId = pathSplits[pathSplits.index('dp') + 1]
    except Exception as E:
        print('Error on url: {}'.format(url))
        print(E)
    return prodId

if __name__ == '__main__':
    from fake_useragent import UserAgent
    agents = UserAgent()

    scrap('https://www.amazon.de/s?me=A3B6Q99ITZLBDT&marketplaceID=A1PA6795UKMFR9', agents.random)

    # with open('temp/sample_dump.html', 'r') as file:
    #     getLinks(bs(file.read(), 'html5lib'))