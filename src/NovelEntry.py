from dataclasses import dataclass, field

@dataclass(init=True, repr=True)
class NovelEntry:
    number: int = -1
    country: str = ""
    title: str = ""
    url: str = ""
    chapters_completed: str = ""
    rating: str = ""
    reading_status: str = ""
    genre: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    date_modified: str = ""
    notes: str = ""
    novel_type: str = ""    