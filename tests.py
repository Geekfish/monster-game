import unittest

from hamcrest import *

from game import Game

def is_not_in(collection):
    return not is_in(collection)


class TestGameFunctions(unittest.TestCase):
    def setUp(self):
        Game.DEFAULT_DATA_FILE = 'data/world_test.txt'

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

        city_index = {
            'foo': my_city.south,
            'bar': my_city.west,
            'London': my_city
        }
        assert_that(my_city.to_output(city_index), 'London south=foo west=bar')

    def test_deploy_monsters(self):
        game = Game()
        game.populate_map()
        game.deploy_monsters(10)

        total_occupants = 0
        for city in game.cities:
            total_occupants += len(city.occupants)

        assert_that(total_occupants, is_(10))

    def test_city_destroy(self):
        game = Game()
        game.populate_map()

        city = game.cities[0]
        game.monsters.append(Game.Monster(1, city))
        game.monsters.append(Game.Monster(2, city))

        game.destroy_city(city)

        assert_that(len(game.monsters), is_(0))
        assert_that(city, is_not_in(game.cities))
        assert_that(city.name, is_not_in(game.city_index.keys()))



    def test_check_game_ending_conditions(self):
        game = Game()

        game.cities = [1,2,3]
        game.monsters = []
        assert_that(game.check_game_ending_conditions(), is_(True))

        game.cities = []
        game.monsters = []
        assert_that(game.check_game_ending_conditions(), is_(True))

        game.cities = [1,2,3]
        game.monsters = [1,]
        assert_that(game.check_game_ending_conditions(), is_(False))

    def get_city_with_neighbours(self):
        city1 = Game.City({'city_name': 'A'})
        city2 = Game.City({'city_name': 'B'})
        city3 = Game.City({'city_name': 'C'})
        city4 = Game.City({'city_name': 'D'})

        city1.south = city2
        city1.north = city3
        city1.west = city4

        return city1

    def test_available_travel_directions(self):
        city = self.get_city_with_neighbours()
        assert_that(city.available_travel_directions, is_(['north', 'south', 'west']))

    def test_monster_move(self):
        city = self.get_city_with_neighbours()
        monster = Game.Monster(1, city)
        previous_city = monster.current_city
        monster.move()

        assert_that(monster.current_city, is_not(previous_city))

        city = self.get_city_with_neighbours()
        monster = Game.Monster(1, city)

        previous_city = monster.current_city
        previous_city.north = None
        previous_city.south = None
        previous_city.east = None
        previous_city.west = None

        monster.move()

        assert_that(monster.current_city, is_(previous_city))

    def test_city_is_overcome(self):
        city = Game.City({'city_name': 'abc'})
        monster1 = Game.Monster(1, city)
        assert_that(not city.is_overcome)

        monster2 = Game.Monster(2, city)
        assert_that(city.is_overcome)

        monster3 = Game.Monster(3, city)
        assert_that(city.is_overcome)

    def test_get_pretty_city_occupants(self):
        city = Game.City({'city_name': 'abc'})
        monster1 = Game.Monster(1, city)
        assert_that(city.get_pretty_occupants(), is_('#1'))

        monster2 = Game.Monster(2, city)
        city.occupants = [monster1, monster2]

        assert_that(city.get_pretty_occupants(), is_('#1 and #2'))

        monster3 = Game.Monster(3, city)
        assert_that(city.get_pretty_occupants(), is_('#1, #2 and #3'))

if __name__ == '__main__':
    unittest.main()
