import queue
import threading
import os
import scraper
import pandas as pd
from time import sleep, time
from fake_useragent import UserAgent

INTERMEDIATE_SLEEP_TIME = 1000 # 200ms
LONG_GAP_AFTER = 50 # after this # of links scraped system will sleep for a longer period
LONG_SLEEP_TIMER = 10000 # 10s

BASE_URL = 'https://www.amazon.de/s?me=A3B6Q99ITZLBDT&marketplaceID=A1PA6795UKMFR9'
PAGINATION_PAGES = 'https://www.amazon.de/s?i=merchant-items&me=A3B6Q99ITZLBDT&page={}&marketplaceID=A1PA6795UKMFR9&qid=1595107300&ref=sr_pg_{}'

SAVE_FILE_PATH = 'data/async_t{}.csv'

AGENTS = UserAgent()

# outputDataframe = pd.DataFrame(columns=['url', 'short_code'])

q = queue.Queue()

def saveData(df, links, threadnumber):
    global outputDataFrame, SAVE_FILE_PATH
    for link in links:
        df.loc[len(df)] = [link, scraper.getProductId(link)]
    df.to_csv(SAVE_FILE_PATH.format(threadnumber), index=False)

def crawler(threadnumber):
    continueScraping = True
    trial = 0
    currentPage = 1

    outputDataframe = pd.DataFrame(columns=['url', 'short_code'])

    while continueScraping:
        url = q.get()
        
        if url is None:
            break
        
        links = []
        try:
            links = scraper.scrape(url, AGENTS.random)
        except Exception as E:
            print(E)
            print('Error scraping url: {}'.format(url))

        if len(links) == 0:
            trial += 1
        else:
            trial = 0
        if trial == 3:
            continueScraping = False

        currentPage += 1
        
        if currentPage % LONG_GAP_AFTER == 0:
            print('SLEEPING FOR {}'.format(LONG_SLEEP_TIMER))
            sleep(LONG_SLEEP_TIMER / 1000)

        saveData(outputDataframe, links, threadnumber)
        sleep(INTERMEDIATE_SLEEP_TIME  / 1000)
        q.task_done()

def startCrawling(numberThread, startNumber, endNumber):    
    threads = []
    
    for i in range(numberThread):
        t = threading.Thread(target=crawler, args=(i+1,))
        t.start()
        threads.append(t)

    for i in range(startNumber, endNumber+1):
        q.put(PAGINATION_PAGES.format(i, i))
    
    q.join()

    for i in range(numberThread):
        q.put(None)
    
    for t in threads:
        t.join()

if __name__ == '__main__':
    startCrawling(5, 4772, 20000)