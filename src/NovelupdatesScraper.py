import os
import string
from dataclasses import dataclass, field
import logging

import cloudscraper
from cloudscraper.exceptions import CloudflareChallengeError
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, filename="logger.log", datefmt='%m/%d/%Y %H:%M:%S',
                    format='%(levelname)s: %(module)s: %(message)s; %(asctime)s')

@dataclass(init=True, repr=True)
class NovelupdatesScraper:
    title: str = ""
    url: str = ""
    html: str = ""
    tags: list = field(default_factory=list)
    genre: list = field(default_factory=list)
    country: string = ""
    novel_type: str = ""
    
    def scrape_from_url(self) -> bool:
        """Scrapes html data from the Novelupdates novel page. Assumes that self.url already has the valid url.

        Returns:
            bool: Whether scraping data from the url succeeded
        """
        logging.info('scrape_from_url')
        if "https://www.novelupdates.com/series/" not in self.url:
            logging.warning(f'Not novelupdates url: {self.url}')
            return False
        try:
            scraper = cloudscraper.create_scraper(
                delay = 10, 
                browser={
                    'browser': 'chrome',
                    'platform': 'android',
                    'desktop': False
                }
            )
            self.html = scraper.get(self.url).text
        except requests.exceptions.MissingSchema:
            logging.warning(f'Invalid url format: {self.url}')
            return False
        except CloudflareChallengeError:
            logging.warning(f'Cloudflare challenge error: {self.url}')
            return False
        logging.info('Web scraping succeeded')
        return self.get_info_from_html()
        
    def import_html(self, filename: str) -> bool:
        """ 
        Args:
            filename (str): A valid Novelupdates novel page html file

        Returns:
            bool: Whether the file was found and info scraping succeeded
        """
        logging.info(f'import_html: {filename}')
        if not os.path.isfile(filename):
            logging.warning(f'Html file does not exist: {filename}')
            return False
        logging.info(f'Html file does exist: {filename}')
        with open(filename, 'r', encoding= 'utf-8', newline='') as f:
            self.html = f.read()
        return self.get_info_from_html()
        
            
    def get_info_from_html(self) -> bool:
        """Assumes that self.html already has html content from a Novelupdates novel page; grabs different novel data values

        Returns:
            bool: Whether scraping html data values succeeded
        """
        try:
            logging.info('get_info_from_html')
            soup = BeautifulSoup(self.html, "html.parser")    
            uncleaned_tags = soup.find_all(id = "etagme")
            self.tags = [i.getText() for i in uncleaned_tags]
            genre_div = soup.find(id = "seriesgenre")
            self.genre = [i.getText() for i in genre_div.findChildren()]
            self.title = soup.find("title").getText().replace(" - Novel Updates", "")
            self.country = soup.find(style = "color:#8D8D8D;").getText()[1:-1] # Gets rid of parenthesis
            self.novel_type = soup.find(class_ = "genre type").getText()
            return True
        except AttributeError:
            logging.warning('Getting info from html failed')
            return False
            
    def dump_html(self, filename) -> None:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write(self.html)
    
if __name__ == "__main__":    
    pass