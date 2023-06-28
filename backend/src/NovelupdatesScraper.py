import cloudscraper
from bs4 import BeautifulSoup
from dataclasses import dataclass
from dataclasses import field
import string
import os

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
    
    def scrape_from_url(self) -> None:
        """Scrapes html data from the Novelupdates novel page. Assumes that self.url already has the valid url.
        """
        scraper = cloudscraper.create_scraper(delay = 6)
        self.html = scraper.get(self.url).text
        self.get_info_from_html()
        
    def import_html(self, filename: str) -> bool:
        """ 
        Args:
            filename (str): A valid Novelupdates novel page html file

        Returns:
            bool: Whether the file was found
        """
        if os.path.isfile(filename):
            with open(filename, 'r', encoding= 'utf-8', newline='') as f:
                self.html = f.read()
            self.get_info_from_html()
            return True
        return False
            
    def get_info_from_html(self) -> None:
        """Assumes that self.html already has html content from a Novelupdates novel page
        """
        soup = BeautifulSoup(self.html, "html.parser")    
        uncleaned_tags = soup.find_all(id = "etagme")
        self.tags = [i.getText() for i in uncleaned_tags]
        genre_div = soup.find(id = "seriesgenre")
        self.genre = [i.getText() for i in genre_div.findChildren()]
        self.title = soup.find("title").getText().replace(" - Novel Updates", "")
        self.country = soup.find(style = "color:#8D8D8D;").getText()[1:-1] # Gets rid of parenthesis
        self.novel_type = soup.find(class_ = "genre type").getText()   
            
    def dump_html(self, filename) -> None:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write(self.html)
    
if __name__ == "__main__":    
    pass