import unittest
import os
import datetime

from src.StoreNovelData import StoreNovelData

class TestDefault(unittest.TestCase):
    def setUp(self):
        files = os.listdir()
        for file in files:
            if file[:4] == 'test' and file[-3:] == '.db':
                os.remove(file)
    
    def test_empty_table(self):
        test = StoreNovelData('test.db')
        created = test.create_table('test')
        selected = test.select_table('test')
        contents = test.dump_table_to_list()
        
        self.assertEqual(created, True)
        self.assertEqual(selected, True)
        self.assertEqual(contents, [])
        os.remove('test.db')
        
    def test_invalid_table(self):
        test = StoreNovelData('test2.db')
        created = test.create_table('test2')
        selected = test.select_table('aslkdfjalsdf')
        contents = test.dump_table_to_list()
        
        self.assertEqual(created, True)
        self.assertEqual(selected, False)
        self.assertEqual(contents, None)
        os.remove('test2.db')
        
    def test_insert_url(self):
        result = [('https://www.novelupdates.com/series/i-shall-seal-the-heavens/', 'CN', 'I Shall Seal the Heavens', '', 
                   None, '', "['Action', 'Adventure', 'Drama', 'Xianxia']",
                   "['Abandoned Children', 'Adapted to Manhua', 'Age Regression', 'Alchemy', 'Amnesia', 'Appearance Changes', 'Appearance Different from Actual Age', 'Artifacts', 'Bloodlines', 'Body Tempering', 'Calm Protagonist', 'Character Growth', 'Cultivation', 'Cunning Protagonist', 'Dao Comprehension', 'Demonic Cultivation Technique', 'Demons', 'Determined Protagonist', 'Devoted Love Interests', 'Fated Lovers', 'Friendship', 'Gods', 'Handsome Male Lead', 'Hard-Working Protagonist', 'Heavenly Tribulation', 'Immortals', 'Legends', 'Long Separations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Marriage', 'Master-Disciple Relationship', 'Money Grubber', 'Monsters', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Mysterious Family Background', 'Near-Death Experience', 'Past Plays a Big Role', 'Pill Concocting', 'Poor to Rich', 'Protagonist with Multiple Bodies', 'Race Change', 'Romantic Subplot', 'Ruthless Protagonist', 'Shameless Protagonist', 'Sharp-tongued Characters', 'Slow Romance', 'Time Manipulation', 'Tragic Past', 'Trickster', 'Underestimated Protagonist', 'Unrequited Love', 'Wars', 'Weak to Strong']",
                   datetime.date.today().strftime("%Y-%m-%d"), '')]
        test = StoreNovelData('test3.db')
        test.create_table('test3')
        test.select_table('test3')
        added = test.add_entry_from_url(url = "https://www.novelupdates.com/series/i-shall-seal-the-heavens/")
        contents = test.dump_table_to_list()
        
        self.assertEqual(added, True)
        self.assertEqual(contents, result)
        os.remove('test3.db')

if __name__ == "__main__":
    unittest.main()