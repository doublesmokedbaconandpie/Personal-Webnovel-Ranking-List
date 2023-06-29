import unittest
import os
import shutil
import datetime

from src.StoreNovelData import StoreNovelData

ORIGIN_DB = 'tests/db_files/ISSTH.db'
ORIGIN_URL = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/"
origin = StoreNovelData(ORIGIN_DB)
origin.delete_table('test')
origin.create_table('test')
origin.select_table('test')
origin.add_entry_from_url(ORIGIN_URL)
origin.dump_table_to_list()

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
        self.expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        
    def test_insert_url(self):
        test = StoreNovelData('test_insert_url.db')
        test.create_table('test')
        test.select_table('test')
        
        added = test.add_entry_from_url(ORIGIN_URL)
        contents = test.dump_table_to_list()
        
        self.assertTrue(added)
        self.assertEqual(contents, self.expected_entry)
    
    def test_insert_url_duplicate(self):
        shutil.copy(ORIGIN_DB, 'test_insert_url_duplicate.db')
        test = StoreNovelData('test_insert_url_duplicate.db')
        test.select_table('test')
        
        added = test.add_entry_from_url(ORIGIN_URL)
        contents = test.dump_table_to_list()
        
        self.assertFalse(added)
        self.assertEqual(contents, self.expected_entry)
    
    def test_fetch_valid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_fetch_valid_entry.db')
        test = StoreNovelData('test_fetch_valid_entry.db')
        test.select_table('test')
        
        test.add_entry_from_url(ORIGIN_URL)
        fetched_contents = test.fetch_entry_from_url(ORIGIN_URL)
        
        self.assertEqual(fetched_contents, self.expected_entry)
    
    def test_fetch_invalid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_fetch_invalid_entry.db')
        test = StoreNovelData('test_fetch_invalid_entry.db')
        test.select_table('test')
        
        url_fetch = "https://www.novelupdates.com/series/reverend-insanity/"
        test.add_entry_from_url(ORIGIN_URL)
        fetched_contents = test.fetch_entry_from_url(url_fetch)
        
        self.assertEqual(fetched_contents, None)
    
    def test_delete_valid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_delete_valid_entry.db')
        test = StoreNovelData('test_delete_valid_entry.db')
        test.select_table('test')
        
        test.add_entry_from_url(ORIGIN_URL)
        deleted = test.delete_entry_from_url(ORIGIN_URL)
        after_delete = test.dump_table_to_list()

        self.assertTrue(deleted)
        self.assertEqual(after_delete, [])
        
    def test_delete_invalid_entry(self):
        shutil.copy(ORIGIN_DB, 'test_delete_invalid_entry.db')
        test = StoreNovelData('test_delete_invalid_entry.db')
        test.select_table('test')
        
        url_delete = "https://www.novelupdates.com/series/reverend-insanity/"
        
        test.add_entry_from_url(ORIGIN_URL)
        deleted = test.delete_entry_from_url(url_delete)
        after_delete = test.dump_table_to_list()
        
        self.assertFalse(deleted)
        self.assertEqual(after_delete, self.expected_entry)
    
    @classmethod
    def tearDownClass(self) -> None:
        files = os.listdir()
        prefixes = ('test_insert', 'test_fetch', 'test_delete')
        for file in files:
            if any(pre in file for pre in prefixes) and file[-3:] == '.db':
                os.remove(file)

class TestUpdateEntry(unittest.TestCase):
    def test_update_url(self):
        expected_entry = [('https://www.novelupdates.com/series/reverend-insanity/', 'CN', 'I Shall Seal the Heavens', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        shutil.copy(ORIGIN_DB, 'test_update_url.db')
        test = StoreNovelData('test_update_url.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'Url', 'https://www.novelupdates.com/series/reverend-insanity/')
        entry = test.fetch_entry_from_url('https://www.novelupdates.com/series/reverend-insanity/')

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)
        
    def test_update_country(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'JP', 'I Shall Seal the Heavens', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        shutil.copy(ORIGIN_DB, 'test_update_country.db')
        test = StoreNovelData('test_update_country.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'Country', "JP")
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
         
    def test_update_title(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'Reverend Insanity', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        shutil.copy(ORIGIN_DB, 'test_update_title.db')
        test = StoreNovelData('test_update_title.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'Title', "Reverend Insanity")
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
             
    def test_update_chapters_completed(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '150', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        shutil.copy(ORIGIN_DB, 'test_update_chapters_completed.db')
        test = StoreNovelData('test_update_chapters_completed.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'ChaptersCompleted', "150")
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                 
    def test_update_rating(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            7, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        shutil.copy(ORIGIN_DB, 'test_update_rating.db')
        test = StoreNovelData('test_update_rating.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'Rating', 7)
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                 
    def test_update_reading_status(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            None, 'No', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        shutil.copy(ORIGIN_DB, 'test_update_reading_status.db')
        test = StoreNovelData('test_update_reading_status.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'ReadingStatus', "No")
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                 
    def test_update_genre(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia, Fantasy']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        shutil.copy(ORIGIN_DB, 'test_update_genre.db')
        test = StoreNovelData('test_update_genre.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'Genre', "['Action', 'Adventure', 'Drama', 'Xianxia, Fantasy']")
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                    
    def test_update_tags(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['TestTag', 'Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), '')]
        shutil.copy(ORIGIN_DB, 'test_update_tags.db')
        test = StoreNovelData('test_update_tags.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'Tags', "['TestTag', 'Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",)
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                   
    def test_update_date_modified(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            "2001-10-10", '')]
        shutil.copy(ORIGIN_DB, 'test_update_date_modified.db')
        test = StoreNovelData('test_update_date_modified.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'DateModified', "2001-10-10")
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
                 
    def test_update_notes(self):
        expected_entry = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
            None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
            "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
            datetime.date.today().strftime("%Y-%m-%d"), 'I have not read this yet lmao ')]
        shutil.copy(ORIGIN_DB, 'test_update_notes.db')
        test = StoreNovelData('test_update_notes.db')
        test.select_table('test')
        
        updated = test.update_entry(ORIGIN_URL, 'Notes', "I have not read this yet lmao ")
        entry = test.fetch_entry_from_url(ORIGIN_URL)

        self.assertTrue(updated)
        self.assertEqual(entry, expected_entry)   
    
    @classmethod      
    def tearDownClass(self) -> None:
        files = os.listdir()
        for file in files:
            if 'test_update' == file[:11] and file[-3:] == '.db':
                os.remove(file)

if __name__ == "__main__":
    files = os.listdir()
    for file in files:
        if file[:4] == 'test' and file[-3:] == '.db':
            os.remove(file)
    unittest.main()
