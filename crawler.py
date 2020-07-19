import scraper
import sys
from fake_useragent import UserAgent
from time import time, sleep
import pandas as pd

INTERMEDIATE_SLEEP_TIME = 200 # 200ms
LONG_GAP_AFTER = 50 # after this # of links scraped system will sleep for a longer period
LONG_SLEEP_TIMER = 10000 # 10s

BASE_URL = 'https://www.amazon.de/s?me=A3B6Q99ITZLBDT&marketplaceID=A1PA6795UKMFR9'
PAGINATION_PAGES = 'https://www.amazon.de/s?i=merchant-items&me=A3B6Q99ITZLBDT&page={}&marketplaceID=A1PA6795UKMFR9&qid=1595107300&ref=sr_pg_{}'

AGENTS = UserAgent()

SAVE_FILE_PATH = 'data/data.csv'

def saveUrl(links):
    pass

def startCrawling(startPage=1,endPage=None):
    currentPage = startPage
    continueScraping = True
    trial = 0

    outputDataframe = pd.DataFrame(columns=['url', 'short_code'])

    while continueScraping:
        print()
        print(f'Current page # {currentPage}')
        if currentPage == 1:
            url = BASE_URL
        else:
            url = PAGINATION_PAGES.format(currentPage, currentPage)

        links = scraper.scrape(url, AGENTS.random)

        if len(links) == 0:
            trial += 1
        else:
            trial = 0
            for link in links:
                outputDataframe.loc[len(outputDataframe)] = [link, scraper.getProductId(link)]
            outputDataframe.to_csv(SAVE_FILE_PATH, index=False)
        if trial == 3:
            continueScraping = False

        if endPage is not None and currentPage == endPage:
            continueScraping = False

        currentPage += 1
        
        if currentPage % LONG_GAP_AFTER == 0:
            print(f'SLEEPING FOR {LONG_SLEEP_TIMER}')
            sleep(LONG_SLEEP_TIMER / 1000)

        sleep(INTERMEDIATE_SLEEP_TIME  / 1000)

        
if __name__ == '__main__':
    startCrawling(startPage=2256)
