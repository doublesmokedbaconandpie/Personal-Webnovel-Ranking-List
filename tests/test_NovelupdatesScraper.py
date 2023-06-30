import unittest
from NovelupdatesScraper import NovelupdatesScraper

class TestDefault(unittest.TestCase):
    def setUp(self):
        self.test = NovelupdatesScraper()       
         
    def test_tags(self):
        self.assertEqual(self.test.tags, [])
    def test_genre(self):
        self.assertEqual(self.test.genre, [])
    def test_title(self):
        self.assertEqual(self.test.title, "")
    def test_country(self):        
        self.assertEqual(self.test.country, "")
    def test_novel_type(self):        
        self.assertEqual(self.test.novel_type, "")
        
class TestInvalidUrlHtml(unittest.TestCase):
    def test_invalid_url(self):
        test = NovelupdatesScraper(url = "akjsdhfjkahsdf")
        url_success = test.scrape_from_url()
        self.assertFalse(url_success)
        
    def test_not_novelupdates(self):
        test = NovelupdatesScraper(url = "https://www.w3schools.com/python/python_try_except.asp")
        url_success = test.scrape_from_url()
        self.assertFalse(url_success)
    
    def test_not_series_novelupdates(self):
        test = NovelupdatesScraper(url = "https://www.novelupdates.com/group/the-sun-is-cold-translations/")
        url_success = test.scrape_from_url()
        self.assertFalse(url_success)
        
    def test_invalid_html(self):
        test = NovelupdatesScraper()
        file_success = test.import_html("tests/html_files/invalidhtml.testhtml")
        self.assertFalse(file_success)

class TestOtonari(unittest.TestCase):
    def setUp(self) -> None:
        self.file = NovelupdatesScraper()
        self.import_success = self.file.import_html("tests/html_files/otonari.testhtml")
        
        self.url = NovelupdatesScraper()
        self.url.url = "https://www.novelupdates.com/series/otonari-no-tenshi-sama-ni-itsu-no-ma-ni-ka-dame-ningen-ni-sareteita-ken-ln/"
        self.scrape_success = self.url.scrape_from_url()
        
    def test_tags(self):
        result_tags = ['Adapted to Anime', 'Adapted to Manga', 'Adapted to Visual Novel', 'Award-winning Work', 'Beautiful Female Lead', 'Calm Protagonist', 'Cold Love Interests', 'Cooking', 'Couple Growth', 'Criminals', 'Cute Story', 'Dense Protagonist', 'Handsome Male Lead', 'Heartwarming', 'Living Alone', 'Male Protagonist', 'Mature Protagonist', 'Modern Day', 'Popular Love Interests', 'R-15', 'Slow Romance']
        self.assertEqual(self.file.tags, result_tags)
    def test_genre(self):
        result_genre = ['Comedy', 'Romance', 'School Life', 'Slice of Life']
        self.assertEqual(self.file.genre, result_genre)
    def test_title(self):
        self.assertEqual(self.file.title, "Otonari no Tenshi-sama ni Itsu no Ma ni ka Dame Ningen ni Sareteita Ken (LN)")
    def test_country(self):        
        self.assertEqual(self.file.country, "JP")
    def test_novel_type(self):        
        self.assertEqual(self.file.novel_type, "Light Novel")
    
    def test_import_success(self):
        self.assertTrue(self.import_success)
    def test_scrape_success(self):
        self.assertTrue(self.scrape_success)
    def test_tags_web_vs_html(self):
        self.assertEqual(self.file.tags, self.url.tags)
    def test_genre_web_vs_html(self):
        self.assertEqual(self.file.genre, self.url.genre)
    def test_title_web_vs_html(self):
        self.assertEqual(self.file.title, self.url.title)
    def test_country_web_vs_html(self):        
        self.assertEqual(self.file.country, self.url.country)
    def test_novel_type_vs(self):        
        self.assertEqual(self.file.novel_type, self.url.novel_type)

class TestLotm(unittest.TestCase):
    def setUp(self) -> None:
        self.file = NovelupdatesScraper()
        self.import_success = self.file.import_html("tests/html_files/lotm.testhtml")
        
    def test_tags(self):
        result_tags = ['Ability Steal', 'Absent Parents', 'Acting', 'Adapted to Drama CD', 'Adapted to Game', 'Adapted to Manhua', 'Alchemy', 'Alternate World', 'Aristocracy', 'Artifacts', 'Assassins', 'Award-winning Work', 'Calm Protagonist', 'Caring Protagonist', 'Cautious Protagonist', 'Character Growth', 'Clever Protagonist', 'Comedic Undertone', 'Cooking', 'Cunning Protagonist', 'Curses', 'Dark', 'Death', 'Death of Loved Ones', 'Depictions of Cruelty', 'Destiny', 'Detectives', 'Determined Protagonist', 'Dolls/Puppets', 'Dragons', 'Eidetic Memory', 'Elves', 'Evil Gods', 'Evil Organizations', 'Evil Religions', 'Familial Love', 'Family', 'Fantasy Creatures', 'Fantasy World', 'Fast Learner', 'Firearms', 'Ghosts', 'God Protagonist', 'Goddesses', 'Godly Powers', 'Gods', 'Hard-Working Protagonist', 'Harsh Training', 'Hidden Abilities', 'Hiding True Abilities', 'Hiding True Identity', 'Hunters', 'Immortals', 'Industrialization', 'Kingdoms', 'Lost Civilizations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Manipulative Characters', 'Mature Protagonist', 'Mind Break', 'Mind Control', 'Misunderstandings', 'Money Grubber', 'Monsters', 'Multiple Identities', 'Multiple POV', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Murders', 'Mutated Creatures', 'Mysterious Past', 'Mystery Solving', 'Mythical Beasts', 'Mythology', 'Nightmares', 'Nobles', 'Parasites', 'Past Plays a Big Role', 'Pets', 'Philosophical', 'Pirates', 'Police', 'Polite Protagonist', 'Proactive Protagonist', 'Protagonist with Multiple Bodies', 'Puppeteers', 'Religions', 'Resurrection', 'Righteous Protagonist', 'Saints', 'Schemes And Conspiracies', 'Sealed Power', 'Secret Identity', 'Secret Organizations', 'Secrets', 'Sentient Objects', 'Shapeshifters', 'Skill Assimilation', 'Slow Growth at Start', 'Souls', 'Special Abilities', 'Spirits', 'Strategic Battles', 'Thriller', 'Time Skip', 'Transformation Ability', 'Transmigration', 'Transplanted Memories', 'Trickster', 'Vampires', 'Wars', 'Weak to Strong', 'Wealthy Characters', 'Werebeasts', 'Zombies']
        self.assertEqual(self.file.tags, result_tags)
    def test_genre(self):
        result_genre = ['Comedy', 'Horror', 'Mature', 'Mystery', 'Psychological', 'Supernatural']
        self.assertEqual(self.file.genre, result_genre)
    def test_title(self):
        self.assertEqual(self.file.title, "Lord of the Mysteries")
    def test_country(self):        
        self.assertEqual(self.file.country, "CN")
    def test_novel_type(self):        
        self.assertEqual(self.file.novel_type, "Web Novel")

class TestYoukoso(unittest.TestCase):
    def setUp(self) -> None:
        self.file = NovelupdatesScraper()
        self.import_success = self.file.import_html("tests/html_files/youkoso.testhtml")
        
    def test_tags(self):
        result_tags = ['Academy', 'Adapted to Anime', 'Adapted to Manga', 'Anti-social Protagonist', 'Antihero Protagonist', 'Apathetic Protagonist', 'Arrogant Characters', 'Award-winning Work', 'Awkward Protagonist', 'Beautiful Female Lead', 'Blackmail', 'Calm Protagonist', 'Cautious Protagonist', 'Character Growth', 'Clever Protagonist', 'Cold Protagonist', 'Cruel Characters', 'Cunning Protagonist', 'Different Social Status', 'Distrustful Protagonist', 'Fearless Protagonist', 'Genius Protagonist', 'Handsome Male Lead', 'Hiding True Abilities', 'Hiding True Identity', 'Love Interest Falls in Love First', 'Male Protagonist', 'Manipulative Characters', 'Mature Protagonist', 'Modern Day', 'Multiple POV', 'Mysterious Past', 'Overpowered Protagonist', 'Past Plays a Big Role', 'Philosophical', 'Proactive Protagonist', 'Protagonist Strong from the Start', 'Romantic Subplot', 'Ruthless Protagonist', 'Schemes And Conspiracies', 'Secretive Protagonist', 'Slow Romance', 'Stoic Characters', 'Strategic Battles', 'Strategist', 'Strength-based Social Hierarchy', 'Teamwork', 'Tragic Past', 'Underestimated Protagonist', 'Unreliable Narrator']
        self.assertEqual(self.file.tags, result_tags)
    def test_genre(self):
        result_genre = ['Drama', 'Psychological', 'School Life', 'Shounen', 'Slice of Life']
        self.assertEqual(self.file.genre, result_genre)
    def test_title(self):
        self.assertEqual(self.file.title, "Youkoso Jitsuryoku Shijou Shugi no Kyoushitsu e")
    def test_country(self):        
        self.assertEqual(self.file.country, "JP")
    def test_novel_type(self):        
        self.assertEqual(self.file.novel_type, "Light Novel")   

if __name__ == "__main__":
    unittest.main()