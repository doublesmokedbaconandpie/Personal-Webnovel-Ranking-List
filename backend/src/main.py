import cloudscraper
from bs4 import BeautifulSoup
import string

# input novelname
# get url somehow
# in future allow for URL directly option
# scrape
# return tags

def dump_html(thing: string) -> None:
    with open('test.html', 'w') as f:
        f.write(thing)

def get_tags_from_url(url: string) -> list:
    scraper = cloudscraper.create_scraper(delay = 6)
    response_text: string = scraper.get(url).text
    dump_html(response_text)
    
    

if __name__ == "__main__":
    tmpurl = "https://www.novelupdates.com/series/otonari-no-tenshi-sama-ni-itsu-no-ma-ni-ka-dame-ningen-ni-sareteita-ken-wn/"
    get_tags_from_url(tmpurl)