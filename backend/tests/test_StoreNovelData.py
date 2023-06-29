import unittest
import os
import shutil
import datetime

from src.StoreNovelData import StoreNovelData

ORIGIN_DB = 'tests/db_files/ISSTH.db'

class TestTable(unittest.TestCase):
    def test_empty_table(self):
        test = StoreNovelData('test_empty_table.db')
        created = test.create_table('test')
        selected = test.select_table('test')
        contents = test.dump_table_to_list()
        
        self.assertTrue(created)
        self.assertTrue(selected)
        self.assertEqual(contents, [])
        
    def test_invalid_table(self):
        test = StoreNovelData('test_invalid_table.db')
        created = test.create_table('test')
        selected = test.select_table('aslkdfjalsdf')
        contents = test.dump_table_to_list()
        
        self.assertTrue(created)
        self.assertFalse(selected)
        self.assertIsNone(contents)
    
    @classmethod
    def tearDownClass(self) -> None:
        dbNames = ['test_empty_table.db', 'test_invalid_table.db']
        for db in dbNames:
            os.remove(db)

class TestInsertDeleteFetch(unittest.TestCase):        
    def setUp(self):
        self.result = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        
    def test_insert_url(self):
        test = StoreNovelData('test_insert_url.db')
        test.create_table('test')
        test.select_table('test')
        
        added = test.add_entry_from_url(url = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/")
        contents = test.dump_table_to_list()
        
        self.assertTrue(added)
        self.assertEqual(contents, self.result)
    
    def test_insert_url_duplicate(self):
        shutil.copy(ORIGIN_DB, 'test_insert_url_duplicate.db')
        test = StoreNovelData('test_insert_url_duplicate.db')
        test.select_table('test')
        
        added = test.add_entry_from_url(url = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/")
        contents = test.dump_table_to_list()
        
        self.assertFalse(added)
        self.assertEqual(contents, self.result)
    
    def test_fetch_valid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_fetch_valid_entry.db')
        test = StoreNovelData('test_fetch_valid_entry.db')
        test.select_table('test')
        
        url = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/"
        test.add_entry_from_url(url)
        fetched_contents = test.fetch_url_entry(url)
        
        self.assertEqual(fetched_contents, self.result)
    
    def test_fetch_invalid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_fetch_invalid_entry.db')
        test = StoreNovelData('test_fetch_invalid_entry.db')
        test.select_table('test')
        
        url_add = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/"
        url_fetch = "https://www.novelupdates.com/series/reverend-insanity/"
        test.add_entry_from_url(url_add)
        fetched_contents = test.fetch_url_entry(url_fetch)
        
        self.assertEqual(fetched_contents, None)
    
    def test_delete_valid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_delete_valid_entry.db')
        test = StoreNovelData('test_delete_valid_entry.db')
        test.select_table('test')
        
        url = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/"
        test.add_entry_from_url(url)
        deleted = test.delete_url(url)
        after_delete = test.dump_table_to_list()

        self.assertTrue(deleted)
        self.assertEqual(after_delete, [])
        
    def test_delete_invalid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_delete_invalid_entry.db')
        test = StoreNovelData('test_delete_invalid_entry.db')
        test.select_table('test')
        
        url_add = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/"
        url_delete = "https://www.novelupdates.com/series/reverend-insanity/"
        
        test.add_entry_from_url(url_add)
        deleted = test.delete_url(url_delete)
        after_delete = test.dump_table_to_list()
        
        self.assertEqual(deleted, False)
        self.assertEqual(after_delete, self.result)
    
    @classmethod
    def tearDownClass(self) -> None:
        files = os.listdir()
        prefixes = ('test_insert', 'test_fetch', 'test_delete')
        for file in files:
            if any(pre in file[:11] for pre in prefixes) and file[-3:] == '.db':
                os.remove(file)

if __name__ == "__main__":
    files = os.listdir()
    for file in files:
        if file[:4] == 'test' and file[-3:] == '.db':
            os.remove(file)
    unittest.main()
    
    