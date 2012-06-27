import re

class Game(object):
    DATA_FILE = 'data/world_map_small.txt'

    class City(object):
        NORTH, EAST, WEST, SOUTH = 'north', 'east', 'west', 'south'
        DIRECTIONS = (NORTH, SOUTH, EAST, WEST)

        def __init__(self, attr_dict):
			self.name = attr_dict['city_name']
			self.refs = {}

            for direction in self.DIRECTIONS:
                self.refs[direction] = attr_dict[direction]

        @classmethod
        def get_input_regex(cls):
            return re.compile(cls._compose_regex())

        @classmethod
        def _compose_regex(cls):
            regex = '^(?P<city_name>\w+)'
            for direction in cls.DIRECTIONS:
                regex += "( (%s=)(?P<%s>\w+))?" % (direction, direction)
            return regex

        def as_output(self):
            self.name

        def __str__(self):
            return self.name


    def __init__(self):
        # We're going to keep an index where cities will be removed from
        # instead of looking up all the neighbours.
        # With the city object removed using the index, the neighbour association
        # will also turn into null as it will reference the same object.
        # The city name will act as the UID.
        self.city_index = {}
        self.monsters = []

    def _get_world_file_data(self):
        f = open(self.DATA_FILE, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _create_city(self, line):
        r = self.City.get_input_regex().search(line)
        city_attrs = r.groupdict()
        city = self.City(city_attrs)
        self.city_index[city_attrs['city_name']] = city
        return city

    def populate_map(self):
        lines = self._get_world_file_data()
        self.cities = [self._create_city(line) for line in lines]



if __name__ == '__main__':
    # todo add argparse
    game = Game()
    game.populate_map()
