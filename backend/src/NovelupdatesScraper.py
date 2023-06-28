import os
import string
from dataclasses import dataclass, field
import cloudscraper
import requests
from bs4 import BeautifulSoup

@dataclass(init=True, repr=True)
class NovelupdatesScraper:
    title: str = ""
    url: str = ""
    html: str = ""
    tags: list = field(default_factory=list)
    genre: list = field(default_factory=list)
    title: str = ""
    country: string = ""
    novel_type: str = ""
    
    def scrape_from_url(self) -> bool:
        """Scrapes html data from the Novelupdates novel page. Assumes that self.url already has the valid url.

        Returns:
            bool: Whether scraping data from the url succeeded
        """
        if "https://www.novelupdates.com/series/" not in self.url:
            return False
        try:
            scraper = cloudscraper.create_scraper(delay = 6)
            self.html = scraper.get(self.url).text
        except requests.exceptions.MissingSchema:
            return False
        if not self.get_info_from_html():
            return False
        return True
        
    def import_html(self, filename: str) -> bool:
        """ 
        Args:
            filename (str): A valid Novelupdates novel page html file

        Returns:
            bool: Whether the file was found and info scraping succeeded
        """
        if os.path.isfile(filename):
            with open(filename, 'r', encoding= 'utf-8', newline='') as f:
                self.html = f.read()
            if not self.get_info_from_html():
                return False
            return True
        return False
            
    def get_info_from_html(self) -> bool:
        """Assumes that self.html already has html content from a Novelupdates novel page; grabs different novel data values

        Returns:
            bool: Whether scraping html data values succeeded
        """
        try:
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
            return False
            
    def dump_html(self, filename) -> None:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write(self.html)
    
if __name__ == "__main__":    
    pass