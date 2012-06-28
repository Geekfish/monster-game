import unittest

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
        assert_that(number_of_lines_in_file, is_(7))

    def test_create_city(self):
        game = Game()
        city1 = game._create_city('Hello north=Yes south=This east=Is west=Dog')
        city2 = game._create_city('Fizzbuzz south=Fizz east=Buzz')

        assert_that(city1.name, is_('Hello'))
        assert_that(city1.refs['south'], is_('This'))
        assert_that(city2.refs['east'], is_('Buzz'))
        assert_that(city2.refs['north'], is_(none()))

        city_with_hyphens = game._create_city('This-was south=a-bug')
        assert_that(city_with_hyphens.name, is_('This-was'))
        assert_that(city_with_hyphens.refs['south'], is_('a-bug'))

    def test_populate_neighbours(self):
        game = Game()
        city1 = Game.City({'city_name': 'foo'})
        city2 = Game.City({'city_name': 'bar', 'east': 'foo'})
        game.city_index = {city1.name: city1, city2.name: city2}

        city2.populate_neighbours(game.city_index)
        assert_that(city2.east.name, is_('foo'))

    def test_populate_map(self):
        game = Game()
        game.populate_map()

        assert_that(len(game.cities), is_(7))
        assert_that(len(game.city_index), is_(7))

        first_city = game.cities[0]
        assert_that(first_city.west, is_(instance_of(Game.City)))
        assert_that(first_city.east.name, is_(first_city.refs['east']))

    def test_get_city_regex(self):
        expected_regex = ("^(?P<city_name>[\-\w]+)( (north=)(?P<north>[\-\w]+))?" +
            "( (south=)(?P<south>[\-\w]+))?( (east=)(?P<east>[\-\w]+))?( (west=)(?P<west>[\-\w]+))?")
        assert_that(Game.City._compose_regex(), is_(expected_regex))

    def test_city_to_output(self):
        City = Game.City
        my_city = City({'city_name': 'London'})
        my_city.south = City({'city_name': 'foo'})
        my_city.west = City({'city_name': 'bar'})

        assert_that(my_city.to_output(), 'London south=foo west=bar')

    def test_deploy_monsters(self):
        game = Game()
        game.populate_map()
        game.deploy_monsters(10)

        total_occupants = 0
        for city in game.cities:
            total_occupants += len(city.occupants)

        assert_that(total_occupants, is_(10))


if __name__ == '__main__':
    unittest.main()
