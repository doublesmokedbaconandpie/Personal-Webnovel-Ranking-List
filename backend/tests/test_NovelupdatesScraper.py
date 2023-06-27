import unittest
from src.NovelupdatesScraper import NovelupdatesScraper
import difflib

class TestScrapeNovelupdates(unittest.TestCase):
    def test_default(self):
        test = NovelupdatesScraper()        
        self.assertEqual(test.tags, [])
        self.assertEqual(test.genre, [])
        self.assertEqual(test.country, "")
        self.assertEqual(test.novel_type, "")
        
    @unittest.expectedFailure
    def test_no_get_info_from_html(self):
        result_tags = ['Adapted to Anime', 'Adapted to Manga', 'Adapted to Visual Novel', 'Award-winning Work', 'Beautiful Female Lead', 'Calm Protagonist', 'Cold Love Interests', 'Cooking', 'Couple Growth', 'Criminals', 'Cute Story', 'Dense Protagonist', 'Handsome Male Lead', 'Heartwarming', 'Living Alone', 'Male Protagonist', 'Mature Protagonist', 'Modern Day', 'Popular Love Interests', 'R-15', 'Slow Romance']
        result_genre = ['Comedy', 'Romance', 'School Life', 'Slice of Life']
        test = NovelupdatesScraper()
        test.import_html("tests/html_files/otonari.html")
        
        self.assertEqual(test.tags, result_tags)
        self.assertEqual(test.genre, result_genre)
        self.assertEqual(test.country, "JP")
        self.assertEqual(test.novel_type, "Light Novel")
    
    def test_otonari_file_vs_otonari_web(self):
        test = NovelupdatesScraper()
        test.import_html("tests/html_files/otonari.html")
        file_tags = test.tags
        file_genre = test.genre
        file_country = test.country
        file_novel_type = test.novel_type
        
        test.url = "https://www.novelupdates.com/series/otonari-no-tenshi-sama-ni-itsu-no-ma-ni-ka-dame-ningen-ni-sareteita-ken-ln/"
        test.scrape_from_url()
        web_tags = test.tags
        web_genre = test.genre
        web_country = test.country
        web_novel_type = test.novel_type
        
        self.assertEqual(file_tags, web_tags)
        self.assertEqual(file_genre, web_genre)
        self.assertEqual(file_country, web_country)
        self.assertEqual(file_novel_type, web_novel_type)
    
    def test_otonari_file(self):
        result_tags = ['Adapted to Anime', 'Adapted to Manga', 'Adapted to Visual Novel', 'Award-winning Work', 'Beautiful Female Lead', 'Calm Protagonist', 'Cold Love Interests', 'Cooking', 'Couple Growth', 'Criminals', 'Cute Story', 'Dense Protagonist', 'Handsome Male Lead', 'Heartwarming', 'Living Alone', 'Male Protagonist', 'Mature Protagonist', 'Modern Day', 'Popular Love Interests', 'R-15', 'Slow Romance']
        result_genre = ['Comedy', 'Romance', 'School Life', 'Slice of Life']
        test = NovelupdatesScraper()
        test.import_html("tests/html_files/otonari.html")
        test.get_info_from_html()
        
        self.assertEqual(test.tags, result_tags)
        self.assertEqual(test.genre, result_genre)
        self.assertEqual(test.country, "JP")
        self.assertEqual(test.novel_type, "Light Novel")
    
    def test_lotm_file(self):
        result_tags = ['Ability Steal', 'Absent Parents', 'Acting', 'Adapted to Drama CD', 'Adapted to Game', 'Adapted to Manhua', 'Alchemy', 'Alternate World', 'Aristocracy', 'Artifacts', 'Assassins', 'Award-winning Work', 'Calm Protagonist', 'Caring Protagonist', 'Cautious Protagonist', 'Character Growth', 'Clever Protagonist', 'Comedic Undertone', 'Cooking', 'Cunning Protagonist', 'Curses', 'Dark', 'Death', 'Death of Loved Ones', 'Depictions of Cruelty', 'Destiny', 'Detectives', 'Determined Protagonist', 'Dolls/Puppets', 'Dragons', 'Eidetic Memory', 'Elves', 'Evil Gods', 'Evil Organizations', 'Evil Religions', 'Familial Love', 'Family', 'Fantasy Creatures', 'Fantasy World', 'Fast Learner', 'Firearms', 'Ghosts', 'God Protagonist', 'Goddesses', 'Godly Powers', 'Gods', 'Hard-Working Protagonist', 'Harsh Training', 'Hidden Abilities', 'Hiding True Abilities', 'Hiding True Identity', 'Hunters', 'Immortals', 'Industrialization', 'Kingdoms', 'Lost Civilizations', 'Lucky Protagonist', 'Magic', 'Male Protagonist', 'Manipulative Characters', 'Mature Protagonist', 'Mind Break', 'Mind Control', 'Misunderstandings', 'Money Grubber', 'Monsters', 'Multiple Identities', 'Multiple POV', 'Multiple Realms', 'Multiple Reincarnated Individuals', 'Murders', 'Mutated Creatures', 'Mysterious Past', 'Mystery Solving', 'Mythical Beasts', 'Mythology', 'Nightmares', 'Nobles', 'Parasites', 'Past Plays a Big Role', 'Pets', 'Philosophical', 'Pirates', 'Police', 'Polite Protagonist', 'Proactive Protagonist', 'Protagonist with Multiple Bodies', 'Puppeteers', 'Religions', 'Resurrection', 'Righteous Protagonist', 'Saints', 'Schemes And Conspiracies', 'Sealed Power', 'Secret Identity', 'Secret Organizations', 'Secrets', 'Sentient Objects', 'Shapeshifters', 'Skill Assimilation', 'Slow Growth at Start', 'Souls', 'Special Abilities', 'Spirits', 'Strategic Battles', 'Thriller', 'Time Skip', 'Transformation Ability', 'Transmigration', 'Transplanted Memories', 'Trickster', 'Vampires', 'Wars', 'Weak to Strong', 'Wealthy Characters', 'Werebeasts', 'Zombies']
        result_genre = ['Comedy', 'Horror', 'Mature', 'Mystery', 'Psychological', 'Supernatural']
        test = NovelupdatesScraper()
        test.import_html("tests/html_files/lotm.html")
        test.get_info_from_html()
        
        self.assertEqual(test.tags, result_tags)
        self.assertEqual(test.genre, result_genre)
        self.assertEqual(test.country, "CN")
        self.assertEqual(test.novel_type, "Web Novel")
        
    def test_youkoso_file(self):
        result_tags = ['Academy', 'Adapted to Anime', 'Adapted to Manga', 'Anti-social Protagonist', 'Antihero Protagonist', 'Apathetic Protagonist', 'Arrogant Characters', 'Award-winning Work', 'Awkward Protagonist', 'Beautiful Female Lead', 'Blackmail', 'Calm Protagonist', 'Cautious Protagonist', 'Character Growth', 'Clever Protagonist', 'Cold Protagonist', 'Cruel Characters', 'Cunning Protagonist', 'Different Social Status', 'Distrustful Protagonist', 'Fearless Protagonist', 'Genius Protagonist', 'Handsome Male Lead', 'Hiding True Abilities', 'Hiding True Identity', 'Love Interest Falls in Love First', 'Male Protagonist', 'Manipulative Characters', 'Mature Protagonist', 'Modern Day', 'Multiple POV', 'Mysterious Past', 'Overpowered Protagonist', 'Past Plays a Big Role', 'Philosophical', 'Proactive Protagonist', 'Protagonist Strong from the Start', 'Romantic Subplot', 'Ruthless Protagonist', 'Schemes And Conspiracies', 'Secretive Protagonist', 'Slow Romance', 'Stoic Characters', 'Strategic Battles', 'Strategist', 'Strength-based Social Hierarchy', 'Teamwork', 'Tragic Past', 'Underestimated Protagonist', 'Unreliable Narrator']
        result_genre = ['Drama', 'Psychological', 'School Life', 'Shounen', 'Slice of Life']
        test = NovelupdatesScraper()
        test.import_html("tests/html_files/youkoso.html")
        test.get_info_from_html()
        
        self.assertEqual(test.tags, result_tags)
        self.assertEqual(test.genre, result_genre)
        self.assertEqual(test.country, "JP")
        self.assertEqual(test.novel_type, "Light Novel")

if __name__ == "__main__":
    unittest.main()