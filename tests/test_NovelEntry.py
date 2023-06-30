import unittest

from NovelEntry import NovelEntry

class TestNovelEntryDefault(unittest.TestCase):
    def setUp(self):
        self.novel_entry = NovelEntry()
    def test_number(self):
        self.assertEqual(self.novel_entry.number, -1)
    def test_country(self):
        self.assertEqual(self.novel_entry.country, "")
    def test_title(self):
        self.assertEqual(self.novel_entry.title, "")
    def test_url(self):
        self.assertEqual(self.novel_entry.url, "")
    def test_chapters_completed(self):
        self.assertEqual(self.novel_entry.chapters_completed, "")
    def test_rating(self):
        self.assertEqual(self.novel_entry.rating, "")
    def test_reading_status(self):
        self.assertEqual(self.novel_entry.reading_status, "")
    def test_genre(self):
        self.assertEqual(self.novel_entry.genre, [])
    def test_tags(self):
        self.assertEqual(self.novel_entry.tags, [])
    def test_date_modified(self):
        self.assertEqual(self.novel_entry.date_modified, "")
    def test_notes(self):
        self.assertEqual(self.novel_entry.notes, "")
    def test_novel_type(self):
        self.assertEqual(self.novel_entry.novel_type, "")

class TestNovelEntryAssign(unittest.TestCase):
    def setUp(self):
        self.novel_entry = NovelEntry(number=1, country='1', title='1',url='1',chapters_completed='1',
                                      rating='1', reading_status= '1', genre=['1'], tags=['1'],
                                      date_modified='1', notes='1', novel_type= '1')
    def test_number(self):
        self.assertEqual(self.novel_entry.number, 1)
    def test_country(self):
        self.assertEqual(self.novel_entry.country, "1")
    def test_title(self):
        self.assertEqual(self.novel_entry.title, "1")
    def test_url(self):
        self.assertEqual(self.novel_entry.url, "1")
    def test_chapters_completed(self):
        self.assertEqual(self.novel_entry.chapters_completed, "1")
    def test_rating(self):
        self.assertEqual(self.novel_entry.rating, "1")
    def test_reading_status(self):
        self.assertEqual(self.novel_entry.reading_status, "1")
    def test_genre(self):
        self.assertEqual(self.novel_entry.genre, ['1'])
    def test_tags(self):
        self.assertEqual(self.novel_entry.tags, ['1'])
    def test_date_modified(self):
        self.assertEqual(self.novel_entry.date_modified, "1")
    def test_notes(self):
        self.assertEqual(self.novel_entry.notes, "1")
    def test_novel_type(self):
        self.assertEqual(self.novel_entry.novel_type, "1")
        
if __name__ == "__main__":
    unittest.main()
