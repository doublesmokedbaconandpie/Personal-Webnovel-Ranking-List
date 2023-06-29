import unittest
import os
import datetime

from src.StoreNovelData import StoreNovelData

class TestTable(unittest.TestCase):
    def setUp(self):
        files = os.listdir()
        for file in files:
            if file[:4] == 'test' and file[-3:] == '.db':
                os.remove(file)
    
    def test_empty_table(self):
        test = StoreNovelData('test_empty_table.db')
        created = test.create_table('test')
        selected = test.select_table('test')
        contents = test.dump_table_to_list()
        
        self.assertEqual(created, True)
        self.assertEqual(selected, True)
        self.assertEqual(contents, [])
        os.remove('test_empty_table.db')
        
    def test_invalid_table(self):
        test = StoreNovelData('test_invalid_table.db')
        created = test.create_table('test')
        selected = test.select_table('aslkdfjalsdf')
        contents = test.dump_table_to_list()
        
        self.assertEqual(created, True)
        self.assertEqual(selected, False)
        self.assertEqual(contents, None)
        os.remove('test_invalid_table.db')

class TestInsertDelete(unittest.TestCase):
    def setUp(self):
        files = os.listdir()
        for file in files:
            if file[:4] == 'test' and file[-3:] == '.db':
                os.remove(file)
                
    def test_insert_url(self):
        result = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
                   None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
                   "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
                   datetime.date.today().strftime("%Y-%m-%d"), '')]
        test = StoreNovelData('test_insert_url.db')
        test.create_table('test')
        test.select_table('test')
        added = test.add_entry_from_url(url = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/")
        contents = test.dump_table_to_list()
        
        self.assertEqual(added, True)
        self.assertEqual(contents, result)
        os.remove('test_insert_url.db')
    
    def test_delete_nonexisting_entry(self):
        result = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
                   None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
                   "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
                   datetime.date.today().strftime("%Y-%m-%d"), '')]
        test = StoreNovelData('test_delete_nonexisting_entry.db')
        test.create_table('test')
        test.select_table('test')
        url_add = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/"
        url_delete = "https://www.novelupdates.com/series/reverend-insanity/"
        added = test.add_entry_from_url(url_add)
        before_delete = test.dump_table_to_list()
        deleted = test.delete_url(url_delete)
        after_delete = test.dump_table_to_list()
        
        self.assertEqual(added, True)
        self.assertEqual(before_delete, result)
        self.assertEqual(deleted, False)
        self.assertEqual(after_delete, result)
        os.remove('test_delete_nonexisting_entry.db')
    
    def test_delete_existing_entry(self):
        result = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
                   None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
                   "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
                   datetime.date.today().strftime("%Y-%m-%d"), '')]
        test = StoreNovelData('test_delete_existing_entry.db')
        test.create_table('test')
        test.select_table('test')
        url = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/"
        added = test.add_entry_from_url(url)
        before_delete = test.dump_table_to_list()
        deleted = test.delete_url(url)
        after_delete = test.dump_table_to_list()
        
        self.assertEqual(added, True)
        self.assertEqual(before_delete, result)
        self.assertEqual(deleted, True)
        self.assertEqual(after_delete, [])
        os.remove('test_delete_existing_entry.db')
    

if __name__ == "__main__":
    unittest.main()