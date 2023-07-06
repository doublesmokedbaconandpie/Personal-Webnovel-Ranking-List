from dataclasses import dataclass, field

@dataclass(init=True, repr=True)
class NovelEntry:
    number: int = -1
    url: str = ""
    country: str = ""
    title: str = ""
    chapters_completed: str = ""
    rating: str = ""
    reading_status: str = ""
    genre: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    date_modified: str = ""
    notes: str = ""
    novel_type: str = ""    
    id: int = -1
    
    def assign_vals_from_tuple(self, i, entry: tuple):
        self.number = str(i + 1) + '.'
        self.url = entry[0]
        self.country = entry[1]
        self.title = entry[2]
        self.chapters_completed = entry[3]
        self.rating = entry[4]
        self.reading_status = entry[5]
        self.genre = entry[6]
        self.tags = entry[7]
        self.date_modified = entry[8]
        self.notes = entry[9]
        self.id = entry[10]
    
    @staticmethod
    def is_valid_col(col):
        valid_cols = ['Country', 'Title','Url','Chapters Completed','Rating (Out of 10)','Reading Status', 'Genre','Tags','Date Modified','Notes']
        return col in valid_cols
        
    @staticmethod
    def get_col_num(col) -> int:
        valid_cols = ['Country', 'Title','Url','Chapters Completed','Rating (Out of 10)','Reading Status', 'Genre','Tags','Date Modified','Notes']
        if col not in valid_cols:
            return -1
        return valid_cols.index(col)
    
    @staticmethod
    def conv_web_col_to_server_col(col) -> str:
        valid_cols = {'Country': 'Country',
                      'Title': 'Title',
                      'Url': 'Url',
                      'Chapters Completed': 'ChaptersCompleted',
                      'Rating (Out of 10)': 'Rating',
                      'Reading Status': 'ReadingStatus',
                      'Genre': 'Genre',
                      'Tags': 'Tags',
                      'Date Modified': "DateModified",
                      'Notes': 'Notes'} # ID not included because ID shouldn't be edited from client
        return valid_cols[col]
