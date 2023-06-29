import sqlite3
from datetime import date
from src.NovelupdatesScraper import NovelupdatesScraper
# from NovelupdatesScraper import NovelupdatesScraper

class StoreNovelData:
    def __init__(self, DBname: str) -> None:
        """Creates a database connection. Since this is a URL database, columns are planned as ("url", "status", "archived"). Use select_table() 
        to choose an active table
        
        (Country, Title, Chapters Completed, Rating, Reading?, Genre, Tags, Date Modified, Notes)

        Args:
            DBname (str): name of database
        """
        
        self.DBname: str = DBname
        self.conn: sqlite3.Connection = sqlite3.connect(DBname)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.index_active: bool = False
        self.table_name: str = ""
        
    def select_table(self, table_name: str) -> bool:
        """Sets an active table

        Args:
            table_name (str): table to be active

        Returns:
            bool: whether the table was selected
        """
        
        if not self.table_exists(table_name):
            return False
        self.table_name = table_name
        return True
    
    def create_table(self, table_name: str) -> bool:
        """Creates a table in the DB; automatically selects it too

        Args:
            table_name (str): candidate table name
            columns (tuple): columns in the table

        Returns:
            bool: whether a new table is added
        """
        
        if self.table_exists(table_name):
            return False
        self.cursor.execute(f'''CREATE TABLE {table_name} (
            Url TEXT, Country TEXT, Title TEXT, ChaptersCompleted TEXT, Rating INTEGER,
            ReadingStatus TEXT, Genre TEXT, Tags TEXT, DateModified TEXT, Notes TEXT)''')
        self.conn.commit()
        return True
    
    def exists_url_entry(self, url: str) -> bool:
        """Returns if a url's row exists in a specific table

        Args:
            url (str): url
        """
        if not self.table_name:
            return False
        params = (url,)
        result = self.cursor.execute(f"SELECT url FROM {self.table_name} WHERE url = ?", params).fetchall()
        return bool(result)
    
    def add_entry_from_url(self, url: str) -> bool:
        """Saves a url into a table

        Args:
            url (str): url added
            status (str, optional): Current status of url. Can be: Exists, Not Exists, No Internet, Renamed. Defaults to "".
            archived (bool, optional): If url is archived to archive.org. Defaults to False.

        Returns:
            bool: Whether the url was successfully added to the table
        """
        if self.exists_url_entry(url) or not self.table_name:
            return False
        
        novel = NovelupdatesScraper(url=url)
        novel.scrape_from_url()
        
        # (Url TEXT, Country TEXT, Title TEXT, ChaptersCompleted TEXT, Rating INTEGER,
        # ReadingStatus TEXT, Genre TEXT, Tags TEXT, DateModified TEXT, Notes TEXT)
        params = (url, novel.country, novel.title, '', None, '', str(novel.genre), str(novel.tags), date.today().strftime("%Y-%m-%d"), '')
        self.cursor.execute(f"INSERT INTO {self.table_name} VALUES(?,?,?,?,?,?,?,?,?,?)", params)
        self.conn.commit()
        return True
    
    def delete_url(self, url: str) -> bool:
        """Deletes a url from a table

        Args:
            url (str): url to be deleted

        Returns:
            bool: Whether the url was successfully deleted from the table
        """
        
        if not self.exists_url_entry(url) or not self.table_name:
            return False
        
        command_string = f"DELETE FROM {self.table_name} WHERE url='{url}'"
        self.cursor.execute(command_string)
        self.conn.commit()
        return True
    
    def fetch_url_entry(self, url: str):
        # if not self.exists_url_entry(url) or not self.table_name:
        #     return None
        
        params = (url, )
        return self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE Url = ?", params).fetchall()
    
    def update_entry(self, curr_url: str, column: str, val) -> bool:
        valid_columns = ('Url', 'Country', 'Title', 'ChaptersCompleted', 'Rating', 
                         'ReadingStatus', 'Genre', 'Tags', 'DateModified', 'Notes')
        if column not in valid_columns or not self.exists_url_entry(curr_url):
            return False
        self.conn.commit()
        return True
    
    def dump_table_to_list(self) -> list:
        if not self.table_name:
            return None
        return self.cursor.execute(f"SELECT * FROM {self.table_name}").fetchall()
    
    def close_database(self) -> None:
        """Self explanatory
        """
        
        self.conn.commit()
        self.conn.close()   
        
    def table_exists(self, table_name: str) -> bool:
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall() # list of tuples
        return (table_name,) in tables   
        
if __name__ == "__main__":
    pass