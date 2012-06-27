import unittest

# Sorry for the extra requirement
# makes tests so much nicer to read and write
from hamcrest import *

from game import Game

class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        Game.DATA_FILE = 'data/world_test.txt'

    def test_get_world_file_data(self):
        game = Game()
        file_data = game._get_world_file_data()
        number_of_lines_in_file = len(game._get_world_file_data())

        assert_that(file_data, is_(not_none()))
        assert_that(number_of_lines_in_file, is_(4))

    def test_create_city(self):
        game = Game()
        city1 = game._create_city('Hello north=Yes south=This east=Is west=Dog')
        city2 = game._create_city('Fizzbuzz south=Is east=Easier')

        assert_that(city1.name, is_('Hello'))
        assert_that(city1.refs['south'], is_('This'))
        assert_that(city2.refs['east'], is_('Easier'))
        assert_that(city2.refs['north'], is_(none()))

    def test_populate_map(self):
        game = Game()
        game.populate_map()

        assert_that(len(game.cities), is_(4))
        assert_that(len(game.city_index), is_(4))
    
    def test_get_city_regex(self):
        expected_regex = ("^(?P<city_name>\w+)( (north=)(?P<north>\w+))?" +
            "( (south=)(?P<south>\w+))?( (east=)(?P<east>\w+))?( (west=)(?P<west>\w+))?")
        assert_that(Game.City._compose_regex(), is_(expected_regex))


if __name__ == '__main__':
    unittest.main()
