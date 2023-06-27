import cloudscraper
from bs4 import BeautifulSoup
import string
import os
import difflib

def dump_html(thing: string) -> None:
    with open('test.html', 'w') as f:
        f.write(thing)

class NovelupdatesScraper:
    def __init__(self) -> None:
        self.title: str = ""
        self.url: str = ""
        self.html: str = ""
        
        self.genre: list = []
        self.tags: list = []
        self.novel_type: str = ""
        self.country: string = ""
    
    def scrape_from_url(self) -> None:
        """Scrapes html data from the Novelupdates novel page. Assumes that self.url already has the valid url.
        """
        scraper = cloudscraper.create_scraper(delay = 6)
        self.html = scraper.get(self.url).text
        
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
            return True
        return False
            
    def get_info_from_html(self) -> None:
        """Assumes that self.html already has html content from a Novelupdates novel page
        """
        soup = BeautifulSoup(self.html, "html.parser")    
        uncleaned_tags = soup.find_all(id = "etagme")
        self.tags = [i.getText() for i in uncleaned_tags]
        self.novel_type = soup.find(class_ = "genre type").getText()   
        self.country = soup.find(style = "color:#8D8D8D;").getText()[1:-1] # Gets rid of parenthesis
        genre_div = soup.find(id = "seriesgenre")
        self.genre = [i.getText() for i in genre_div.findChildren()]
            
    def dump_html(self, filename) -> None:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write(self.html)
    
if __name__ == "__main__":
    pass
    # otonari = NovelupdatesScraper()
    # # otonari.url = "https://www.novelupdates.com/series/otonari-no-tenshi-sama-ni-itsu-no-ma-ni-ka-dame-ningen-ni-sareteita-ken-ln/"
    # # otonari.scrape_from_url()
    # # old = otonari.html
    # # otonari.dump_html("otonari.html")
    # otonari.import_html("otonari.html")
    # # new = otonari.html
    
    # # print(new == old)
    # # output_list = [li for li in difflib.ndiff(old, new) if li[0] != ' ']
    # # print(output_list)
    # otonari.get_info_from_html()
    # print(otonari.tags)
    # print(otonari.novel_type)
    # print(otonari.country)
    # print(otonari.genre)
    
    lotm = NovelupdatesScraper()
    lotm.url = "https://www.novelupdates.com/series/lord-of-the-mysteries/"
    lotm.scrape_from_url()
    lotm.dump_html('lotm.html')
    lotm.get_info_from_html()
    print(lotm.tags)
    # print(lotm.novel_type)
    # print(lotm.country)
    print(lotm.genre)
    
    youkoso = NovelupdatesScraper()
    youkoso.url = "https://www.novelupdates.com/series/youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e/"
    youkoso.scrape_from_url()
    youkoso.dump_html("youkoso.html")
    # youkoso.import_html('../tests/otonari.html')
    youkoso.get_info_from_html()
    print(youkoso.tags)
    # # print(youkoso.novel_type)
    # # print(youkoso.country)
    print(youkoso.genre)