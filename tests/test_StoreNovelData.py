import unittest
import os
import shutil
import datetime

from StoreNovelData import StoreNovelData
from NovelEntry import NovelEntry

ORIGIN_DB = 'tests/db_files/ISSTH.db'
ORIGIN_URL = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/"
test_entry = ('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', '', '',
              "['Action', 'Adventure', 'Drama', 'Xianxia']", "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
              datetime.date.today().strftime("%Y-%m-%d"), '', 0)

origin = StoreNovelData(ORIGIN_DB)
origin.delete_table('test')
origin.create_table('test')
origin.select_table('test')
# origin.add_entry_from_url(ORIGIN_URL)
params = NovelEntry()
params.assign_vals_from_tuple(test_entry)
origin.add_full_entry(params)
# origin.cursor.execute(f"INSERT INTO {origin.table_name} VALUES(?,?,?,?,?,?,?,?,?,?,?)", test_entry)
origin.close_database()

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
        dbNames = ['test_empty_table.db', 'test_invalid_table.db', 'ID-test_empty_table-test.ID', 'ID-testsdb_filesISSTH-test.ID' ]
        for db in dbNames:
            os.remove(db)

class TestInsertDeleteFetch(unittest.TestCase):        
    def setUp(self):
        raw_tuple = ('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            '', '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '', 0)
        tmp = NovelEntry()
        tmp.assign_vals_from_tuple(raw_tuple)
        tmp.number = '1.'
        self.expected_entry = [tmp]
        self.invalid_url = "https://www.novelupdates.com/series/reverend-insanity/"
        
    def test_insert_url(self):
        shutil.copy(ORIGIN_DB, 'test_insert_url.db')
        test = StoreNovelData('test_insert_url.db')
        test.select_table('test')
        contents = test.dump_table_to_list()
        
        self.assertEqual(contents, self.expected_entry)
    
    @unittest.skip('no cloudflare')
    def test_insert_url_duplicate(self):
        shutil.copy(ORIGIN_DB, 'test_insert_url_duplicate.db')
        test = StoreNovelData('test_insert_url_duplicate.db')
        test.select_table('test')
        
        added = test.add_entry_from_url(ORIGIN_URL)
        contents = test.dump_table_to_list()
        
        self.assertFalse(added)
        self.assertEqual(contents, self.expected_entry)
    
    def test_exists_entry_valid_url(self):
        shutil.copy(ORIGIN_DB, 'test_exists_entry_valid_url.db')
        test = StoreNovelData('test_exists_entry_valid_url.db')
        test.select_table('test')
        
        exists_entry = test.exists_entry('Url', ORIGIN_URL)

        self.assertTrue(exists_entry)
        
    def test_exists_entry_invalid_url(self):
        shutil.copy(ORIGIN_DB, 'test_exists_entry_invalid_url.db')
        test = StoreNovelData('test_exists_entry_invalid_url.db')
        test.select_table('test')
        
        exists_entry = test.exists_entry('Url', self.invalid_url)

        self.assertFalse(exists_entry)

    def test_exists_entry_valid_ID(self):
        shutil.copy(ORIGIN_DB, 'test_exists_entry_valid_ID.db')
        test = StoreNovelData('test_exists_entry_valid_ID.db')
        test.select_table('test')
        
        exists_entry = test.exists_entry('ID', 0)

        self.assertTrue(exists_entry)

    def test_exists_entry_invalid_ID(self):
        shutil.copy(ORIGIN_DB, 'test_exists_entry_invalid_ID.db')
        test = StoreNovelData('test_exists_entry_invalid_ID.db')
        test.select_table('test')
        
        exists_entry = test.exists_entry('ID', 1)

        self.assertFalse(exists_entry)
        
    def test_fetch_valid_entry_url(self):
        shutil.copy(ORIGIN_DB, 'test_fetch_valid_entry_url.db')
        test = StoreNovelData('test_fetch_valid_entry_url.db')
        test.select_table('test')
        
        fetched_contents = test.fetch_entry('Url', ORIGIN_URL)
        
        self.assertEqual(fetched_contents, self.expected_entry)
        
    def test_fetch_valid_entry_ID(self):
        shutil.copy(ORIGIN_DB, 'test_fetch_valid_entry_ID.db')
        test = StoreNovelData('test_fetch_valid_entry_ID.db')
        test.select_table('test')
        
        fetched_contents = test.fetch_entry('ID', 0)

        self.assertEqual(fetched_contents, self.expected_entry)       
    
    def test_fetch_invalid_entry_url(self):
        shutil.copy(ORIGIN_DB, 'test_fetch_invalid_entry_url.db')
        test = StoreNovelData('test_fetch_invalid_entry_url.db')
        test.select_table('test')
        
        fetched_contents = test.fetch_entry('Url', self.invalid_url)
        
        self.assertEqual(fetched_contents, None)

    def test_fetch_invalid_entry_ID(self):
        shutil.copy(ORIGIN_DB, 'test_fetch_invalid_entry_ID.db')
        test = StoreNovelData('test_fetch_invalid_entry_ID.db')
        test.select_table('test')
        
        fetched_contents = test.fetch_entry('ID', 1)

        self.assertEqual(fetched_contents, None)      

    def test_delete_valid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_delete_valid_entry.db')
        test = StoreNovelData('test_delete_valid_entry.db')
        test.select_table('test')
        
        deleted = test.delete_entry('Url', ORIGIN_URL)
        after_delete = test.dump_table_to_list()

        self.assertTrue(deleted)
        self.assertEqual(after_delete, [])
        
    def test_delete_invalid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_delete_invalid_entry.db')
        test = StoreNovelData('test_delete_invalid_entry.db')
        test.select_table('test')
                
        deleted = test.delete_entry('Url', self.invalid_url)
        after_delete = test.dump_table_to_list()
        
        self.assertFalse(deleted)
        self.assertEqual(after_delete, self.expected_entry)
    
    
    @classmethod
    def tearDownClass(self) -> None:
        files = os.listdir()
        prefixes = ('test_insert', 'test_fetch', 'test_delete', 'test_exists_entry')
        for file in files:
            if any(pre in file for pre in prefixes):
                os.remove(file)

class TestUpdateEntry(unittest.TestCase):
    def setUp(self):
        raw_tuple = ('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            '', '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '', 0)
        tmp = NovelEntry()
        tmp.assign_vals_from_tuple(raw_tuple)
        tmp.number = "1."
        self.default_entry = tmp
    def test_update_url(self):
        expected_entry = self.default_entry
        expected_entry.url = 'https://www.novelupdates.com/series/reverend-insanity/'
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_url.db')
        test = StoreNovelData('test_update_url.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'Url', 'https://www.novelupdates.com/series/reverend-insanity/')
        entry = test.fetch_entry('Url', 'https://www.novelupdates.com/series/reverend-insanity/')

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)
        
    def test_update_country(self):
        expected_entry = self.default_entry
        expected_entry.country = 'JP'
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_country.db')
        test = StoreNovelData('test_update_country.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'Country', "JP")
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
         
    def test_update_title(self):
        expected_entry = self.default_entry
        expected_entry.title = 'Reverend Insanity'
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_title.db')
        test = StoreNovelData('test_update_title.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'Title', "Reverend Insanity")
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
             
    def test_update_chapters_completed(self):
        expected_entry = self.default_entry
        expected_entry.chapters_completed = '150'
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_chapters_completed.db')
        test = StoreNovelData('test_update_chapters_completed.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'ChaptersCompleted', "150")
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                 
    def test_update_rating(self):
        expected_entry = self.default_entry
        expected_entry.rating = '7'
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_rating.db')
        test = StoreNovelData('test_update_rating.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'Rating', '7')
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                 
    def test_update_reading_status(self):
        expected_entry = self.default_entry
        expected_entry.reading_status = 'No'
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_reading_status.db')
        test = StoreNovelData('test_update_reading_status.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'ReadingStatus', "No")
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                 
    def test_update_genre(self):
        expected_entry = self.default_entry
        expected_entry.genre = "['Action', 'Adventure', 'Drama', 'Xianxia, Fantasy']"
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_genre.db')
        test = StoreNovelData('test_update_genre.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'Genre', "['Action', 'Adventure', 'Drama', 'Xianxia, Fantasy']")
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                    
    def test_update_tags(self):
        expected_entry = self.default_entry
        expected_entry.tags = "['TestTag', 'Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']"
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_tags.db')
        test = StoreNovelData('test_update_tags.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'Tags', "['TestTag', 'Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",)
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                   
    def test_update_date_modified(self):
        expected_entry = self.default_entry
        expected_entry.date_modified = "2001-10-10"
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_date_modified.db')
        test = StoreNovelData('test_update_date_modified.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'DateModified', "2001-10-10")
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                 
    def test_update_notes(self):
        expected_entry = self.default_entry
        expected_entry.notes = "I have not read this yet lmao "
        expected_entry = [expected_entry]
        shutil.copy(ORIGIN_DB, 'test_update_notes.db')
        test = StoreNovelData('test_update_notes.db')
        test.select_table('test')
        
        updated = test.update_entry(0, 'Notes', "I have not read this yet lmao ")
        entry = test.fetch_entry('Url', ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
    
    @classmethod      
    def tearDownClass(self) -> None:
        files = os.listdir()
        for file in files:
            if 'test_update' == file[:11] and file[-3:] == '.db':
                os.remove(file)
            if 'ID-test_update' == file[:14]:
                os.remove(file)

if __name__ == "__main__":
    files = os.listdir()
    for file in files:
        if file[:4] == 'test' and file[-3:] == '.db':
            os.remove(file)
    unittest.main()
