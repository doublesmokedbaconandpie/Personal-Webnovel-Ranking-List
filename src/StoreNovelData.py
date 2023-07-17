import sqlite3
from datetime import date
from dataclasses import dataclass
import os
import logging

from NovelupdatesScraper import NovelupdatesScraper
from NovelEntry import NovelEntry

logger = logging.getLogger(__name__)
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, filename="logger.log", datefmt='%m/%d/%Y %H:%M:%S',
                    format='%(levelname)s: %(module)s: %(message)s; %(asctime)s')

class StoreNovelData:
    def __init__(self, DBname: str, altDBname = "", altTable = "") -> None:
        """Creates a database connection. Since this is a URL database, columns are planned as ("url", "status", "archived"). Use select_table() 
        to choose an active table
        
        (Country, Title, Chapters Completed, Rating, Reading?, Genre, Tags, Date Modified, Notes)

        Args:
            DBname (str): name of database
        """
        
        logging.info(f'__init__: {DBname}')
        logging.info(f'__init__: Connecting to altDB: {altDBname}, altTable: {altTable}')
        self.DBname: str = DBname
        self.conn: sqlite3.Connection = sqlite3.connect(DBname)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.index_active: bool = False
        self.table_name: str = ""
        self.id_tracker: IDTracker
        self.valid_columns = ('Url', 'Country', 'Title', 'ChaptersCompleted', 'Rating', 
                         'ReadingStatus', 'Genre', 'Tags', 'DateModified', 'Notes', 'ID')
        self.altDBname = altDBname
        self.altTable = altTable
        
    def select_table(self, table_name: str) -> bool:
        """Sets an active table

        Args:
            table_name (str): table to be active

        Returns:
            bool: whether the table was selected
        """
        logging.info(f'select_table: {table_name}')
        if not self.table_exists(table_name):
            return False
        self.table_name = table_name
        self.set_id_tracker()
        return True
    
    def create_table(self, table_name: str) -> bool:
        """Creates a table in the DB; automatically selects it too

        Args:
            table_name (str): candidate table name
            columns (tuple): columns in the table

        Returns:
            bool: whether a new table is added
        """
        
        logging.info(f'create_table: {table_name}')
        if self.table_exists(table_name):
            return False
        self.cursor.execute(f'''CREATE TABLE {table_name} (
            Url TEXT, Country TEXT, Title TEXT, ChaptersCompleted TEXT, Rating TEXT,
            ReadingStatus TEXT, Genre TEXT, Tags TEXT, DateModified TEXT, Notes TEXT, ID INTEGER)''')
        self.conn.commit()
        return True
    
    def delete_table(self, table_name: str) -> bool:
        """Deletes a table from the DB

        Args:
            table_name (str): table name to be deleted

        Returns:
            bool: whether a table was deleted or not
        """
        logging.info(f'delete_table: {table_name}')
        if not self.table_exists(table_name):
            return False
        
        self.cursor.execute(f"DROP TABLE {table_name}")
        if self.table_name == table_name:
            self.table_name = ""
        self.conn.commit()
        return True
    
    def exists_entry(self, col, val) -> bool:
        """Returns if a row exists in a specific table

        Args:
            col: column in DB
            val: value for respective column        
        """
        logging.info(f'exists_entry')
        if not self.table_name or col not in self.valid_columns:
            logging.info(f'Exit exists_entry: tablename: {self.table_name}, col: {col}')
            return False
        params = (val,)
        result = self.cursor.execute(f"SELECT {col} FROM {self.table_name} WHERE {col}  = ?", params).fetchall()
        logging.info(f'Return exists_entry: col: {col}, val: {val}, result: {result}')
        return bool(result)
    
    def add_entry(self, col, val) -> bool:
        logging.info('add_entry')
        if not self.table_name or col not in self.valid_columns:
            logging.info(f'Exit add_entry: tablename: {self.table_name}, col: {col}')
            return False
        params = ['', '', '', '', '', '', '', '', date.today().strftime("%Y-%m-%d"), '', '']
        index = self.valid_columns.index(col)
        params[index] = val
        params[-1] = self.id_tracker.generate_new_ID()
        params = tuple(params)
        logging.info(f'Return add_entry: Col: {col}, val: {val}, index: {index}, params: {params}')
        self.cursor.execute(f"INSERT INTO {self.table_name} VALUES(?,?,?,?,?,?,?,?,?,?,?)", params)
        self.conn.commit()
        return True
    
    def add_full_entry(self, row: NovelEntry) -> bool:
        logging.info('add_full_entry, row: {row}')
        if not self.table_name or not isinstance(row, NovelEntry):
            logging.info(f'Exit add_full_entry: tablename: {self.table_name}, type(row): {type(row)}')
            return False
        row.id = self.id_tracker.generate_new_ID()
        params = row.return_tuple_from_vals()
        self.cursor.execute(f"INSERT INTO {self.table_name} VALUES(?,?,?,?,?,?,?,?,?,?,?)", params)
        self.conn.commit()
        return True
    
    def add_entry_from_url(self, url: str) -> bool:
        """Saves a url into a table

        Args:
            url: url value

        Returns:
            bool: Whether the url was successfully added to the table
        """
        logging.info(f'add_entry_from_url: {url}')
        if self.exists_entry("Url", url) or not self.table_name:
            logging.info(f'Exit add_entry_from_url: tablename: {self.table_name}')
            return False
        
        novel = NovelupdatesScraper()
        scrape = self.fetch_other_DB_entry(self.altDBname, self.altTable, 'Url', url)
        if scrape:
            novel.country, novel.title, novel.genre, novel.tags = scrape.country, scrape.title, scrape.genre, scrape.tags   
            logging.info(f'Use local cache: altDB: {self.altDBname}, altTable: {self.altTable}')   
            logging.info(f'Scrape info results: {scrape}')            
        else:
            logging.info(f'Webscraping')   
            novel.url = url
            scrape_succeeded = novel.scrape_from_url()
            if not scrape_succeeded:
                logging.info(f'Webscrape failed')
                return False
        
        # (Url TEXT, Country TEXT, Title TEXT, ChaptersCompleted TEXT, Rating INTEGER,
        # ReadingStatus TEXT, Genre TEXT, Tags TEXT, DateModified TEXT, Notes TEXT)
        new_id = self.id_tracker.generate_new_ID()
        params = (url, novel.country, novel.title, '', '', '',
                  str(novel.genre), str(novel.tags), date.today().strftime("%Y-%m-%d"), '', new_id)
        logging.info(f'Execute params: {params}')
        self.cursor.execute(f"INSERT INTO {self.table_name} VALUES(?,?,?,?,?,?,?,?,?,?,?)", params)
        self.conn.commit()
        return True
    
    def delete_entry(self, col, val) -> bool:
        """Deletes a url from a table

        Args:
            col: column in DB
            val: value for respective column

        Returns:
            bool: Whether the url was successfully deleted from the table
        """
        logging.info(f'delete_entry: col: {col}, val: {val}')
        if not self.exists_entry(col, val) or not self.table_name or col not in self.valid_columns:
            logging.info(f'Exit delete_entry: {self.table_name}')
            return False
        
        params = (val, )
        self.cursor.execute( f"DELETE FROM {self.table_name} WHERE {col}=?", params)
        self.conn.commit()
        return True
    
    def fetch_entry(self, col, val) -> list:
        """Returns 

        Args:
            col: column in DB
            val: value for respective column

        Returns:
            list: [(Tuple of column data entries)], None if not found
        """
        logging.info(f'fetch_entry: col: {col}, val: {val}')
        if not self.exists_entry(col, val) or not self.table_name:
            logging.info(f'Exit fetch_entry: tablename: {self.table_name}')
            return None
        
        params = (val, )
        raw_tuple_list = self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE {col} = ?", params).fetchall()
        logging.info(f'fetch_entry len: {len(raw_tuple_list)}')
        NovelEntryList = []
        for i, j in enumerate(raw_tuple_list):
            tmp = NovelEntry()
            tmp.assign_vals_from_tuple(j)
            tmp.number = str(i + 1) + '.'
            NovelEntryList.append(tmp)
        logging.info(f'fetch_entry first: {NovelEntryList[0]}')
        return NovelEntryList
    
    def update_entry(self, ID: int, column: str, val) -> bool:
        """

        Args:
            curr_url (str): Valid url entry in table
            column (str): Valid column in table
            val (str, int): Replacing value (assuming if valid)

        Returns:
            bool: Whether updating was successful
        """
        
        # Note there is no type checking
        
        logging.info(f'update_entry: id: {ID}, column: {column}, val: {val}')
        if column not in self.valid_columns or not self.exists_entry('ID', ID):
            logging.info(f'Exit update_entry')
            return False
        
        params = (val, ID)
        self.cursor.execute(f"UPDATE {self.table_name} SET {column}= ? WHERE ID = ?", params)
        self.conn.commit()
        return True
    
    def update_entry_from_url(self, ID: int, url: str): 
        logging.info(f'update_entry_from_url: id: {ID}, url: {url}')
        if not self.exists_entry("ID", ID) or not self.table_name:
            logging.info(f'Exit update_entry_from_url: tablename {self.table_name}')
            return False
        
        old: NovelEntry = self.fetch_entry("ID", ID)[0]
        logging.info(f'Old entry: {old}')
        novel = NovelupdatesScraper()
        scrape = self.fetch_other_DB_entry(self.altDBname, self.altTable, 'Url', url)
        if scrape:
            novel.country, novel.title, novel.genre, novel.tags = scrape.country, scrape.title, scrape.genre, scrape.tags   
            logging.info(f'Use local cache: altDB: {self.altDBname}, altTable: {self.altTable}')   
            logging.info(f'Scrape info results: {scrape}')            
        else:
            logging.info(f'Webscraping')   
            novel.url = url
            scrape_succeeded = novel.scrape_from_url()
            if not scrape_succeeded:
                logging.info(f'Webscrape failed')
                return False
        
        # (Url TEXT, Country TEXT, Title TEXT, ChaptersCompleted TEXT, Rating INTEGER,
        # ReadingStatus TEXT, Genre TEXT, Tags TEXT, DateModified TEXT, Notes TEXT)
        params = (url, novel.country, novel.title, old.chapters_completed, old.rating, old.reading_status,
                  str(novel.genre), str(novel.tags), date.today().strftime("%Y-%m-%d"), old.notes, ID)
        self.cursor.execute(f"UPDATE {self.table_name} SET \
                            Url = ?, Country = ?, Title = ?, ChaptersCompleted = ?, Rating = ?, ReadingStatus = ?, \
                            Genre = ?, Tags = ?, DateModified = ?, Notes = ?\
                            WHERE ID = ?", params)
        self.conn.commit()
        return True
    
    def add_column(self, column_name: str, type_name: str) -> bool:
        logging.info(f'add_column: column_name: {column_name}, type_name: {type_name}')
        valid_types = ('NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB')
        if column_name not in self.valid_columns or type_name not in valid_types:
            logging.info('Exit add_column')
            return False
        
        self.cursor.execute(f"ALTER TABLE {self.table_name} ADD {column_name} {type_name}")
        self.conn.commit()
        return True
    
    def set_id_tracker(self) -> None:
        self.id_tracker = IDTracker(filename=f"ID-{self.DBname.replace('.db', '').replace('/','')}-{self.table_name}.ID")
        logging.info(f'set_id_tracker: {self.id_tracker}')
    
    def dump_table_to_list(self) -> list:
        if not self.table_name:
            return None
        raw_tuple_list = self.cursor.execute(f"SELECT * FROM {self.table_name}").fetchall()
        NovelEntryList = []
        for i, j in enumerate(raw_tuple_list):
            tmp = NovelEntry()
            tmp.assign_vals_from_tuple(j)
            tmp.number = str(i + 1) + '.'
            NovelEntryList.append(tmp)
        return NovelEntryList
        
    def reset_id_values(self):
        oldList = self.dump_table_to_list()
        new_db = StoreNovelData("replacement.db")
        new_db.create_table(self.table_name)
        new_db.select_table(self.table_name)
        for entry in oldList:
            new_db.add_full_entry(entry)
        self.close_database()
        os.remove(self.DBname)
        os.remove(f"ID-{self.DBname.replace('.db', '').replace('/','')}-{self.table_name}.ID")
        os.rename("replacement.db" , self.DBname)
        os.rename(f"ID-replacement-{self.table_name}.ID",
                  f"ID-{self.DBname.replace('.db', '').replace('/','')}-{self.table_name}.ID")
        self = new_db
    
    def fetch_other_DB_entry(self, altDB: str, altTable: str, col, val):
        # This alternate DB is only meant to store cached novels not part of the stored user experience to avoid needing
        # to fetch requests from the actual Novelupdates site. This alternate DB should never be modified by production code and only
        # done so manually from datasets found elsewhere
        # An example data set is: https://github.com/shhossain/novelupdates-dataset
        logging.info('fetch_other_DB_entry')
        tmp = StoreNovelData(altDB)
        table_exists = tmp.select_table(altTable)
        if not table_exists:
            logging.info(f'Alt table doesnt exist: {altTable}')
            return None
        tmp2 = tmp.fetch_entry(col, val)
        logging.info(f'Fetched Alt table value: {tmp2}')
        if tmp2:
            return tmp2[0]
        return None
    
    def close_database(self) -> None:
        """Self explanatory
        """
        
        self.conn.commit()
        self.conn.close()   
        
    def table_exists(self, table_name: str) -> bool:
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall() # list of tuples
        return (table_name,) in tables   

@dataclass(repr=True)
class IDTracker:
    filename: str = ""
    max_ID: int = -1
    
    def __init__(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.max_ID = int(f.read())  
                self.filename = filename
        else:
            self.filename = filename
            self.set_max_ID(-1)
                    
    def set_max_ID(self, val) -> None:
        if not isinstance(val, int):
            raise TypeError(f'Set_max_ID can only set integers as ID, not "{val}"')
        logging.info(f'set_max_ID: {val}')
        self.max_ID = val
        with open(self.filename, 'w') as f:
            f.write(str(val))
            
    def generate_new_ID(self) -> int:
        logging.info(f'generate_new_ID')
        self.set_max_ID(self.max_ID + 1)
        return self.max_ID
    
if __name__ == "__main__":
    pass