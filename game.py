import re, unittest

class Game(object):
    DATA_FILE = 'data/world_map_small.txt'
    city_regex = re.compile("^(?P<city_name>\w+)( (north=)(?P<north>\w+))?" +
            "( (south=)(?P<south>\w+))?( (east=)(?P<east>\w+))?( (west=)(?P<west>\w+))?")


    class City(object):
        def __init__(self, attr_dict):
            self.name = attr_dict['city_name']
            self.north = attr_dict['north']
            self.east = attr_dict['east']
            self.west = attr_dict['west']
            self.south = attr_dict['south']

        def __str__(self):
            return self.name


    def _get_world_file_data(self):
        f = open(self.DATA_FILE, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _create_city(self, line):
        r = self.city_regex.search(line)
        city_attrs = r.groupdict()
        return self.City(city_attrs)

    def populate_map(self):
        lines = self._get_world_file_data()
        self.cities = [self._create_city(line) for line in lines]


if __name__ == '__main__':
    game = Game()
    game.populate_map()
