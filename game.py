import re, random

class Game(object):
    DATA_FILE = 'data/world_map_small.txt'
    ROUND_LIMIT = 10000
    NUM_MONSTERS = 10

    class Monster(object):
        def __init__(self, ref, starting_city):
            self.name = ref
            self.current_city = starting_city
            self.current_city.occupants.append(self)

        def move(self):
            direction = random.choice(Game.City.DIRECTIONS)
            pass

        def __str__(self):
            return '#' + self.name


    class City(object):
        NORTH, EAST, WEST, SOUTH = 'north', 'east', 'west', 'south'
        DIRECTIONS = (NORTH, SOUTH, EAST, WEST)

        def __init__(self, attr_dict):
            self.name = attr_dict['city_name']
            self.refs = {}
            self.occupants = []
            for direction in self.DIRECTIONS:
                self.refs[direction] = attr_dict.get(direction, None)

        @classmethod
        def get_input_regex(cls):
            return re.compile(cls._compose_regex())

        @classmethod
        def _compose_regex(cls):
            regex = '^(?P<city_name>[\-\w]+)'
            for direction in cls.DIRECTIONS:
                regex += "( (%s=)(?P<%s>[\-\w]+))?" % (direction, direction)
            return regex

        def populate_neighbours(self, city_index):
            for direction in self.DIRECTIONS:
                direction_ref = self.refs.get(direction, None)
                if direction_ref:
                    setattr(self, direction, city_index[direction_ref])

        def to_output(self):
            output = self.name
            for direction in self.DIRECTIONS:
                direction_ref = self.refs[direction]
                if getattr(self, direction, False) and direction_ref:
                    output += " %s=%s" % (direction, direction_ref)
            return output

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

        # set up objects and identifiers
        self.cities = [self._create_city(line) for line in lines]

        # set up neighbour object references
        [city.populate_neighbours(self.city_index) for city in self.cities]

    def deploy_monsters(self, num_monsters):
        self.monsters = []
        # monster #0 would sound bad so we start at #1
        for i in range(1, num_monsters+1):
            random_city = random.choice(self.cities)
            self.monsters.append(Game.Monster(i, random_city))
            print '#%d %s' % (i, random_city)


    def show_result(self):
        for city in self.cities:
            print city.to_output()

    def run(self):
        for tick in range(0, self.ROUND_LIMIT):
            pass


if __name__ == '__main__':
    # todo add argparse
    # todo get num monsters

    # Get set
    game = Game()
    game.populate_map()
    game.deploy_monsters(Game.NUM_MONSTERS)

    # GO!
    game.run()

    game.show_result()
