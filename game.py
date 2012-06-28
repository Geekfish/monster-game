import re, random, argparse, sys

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
            available_directions = self.current_city.available_travel_directions
            if available_directions:
                # if the monster can travel, update the occupants
                # in both current and destination cities
                direction = random.choice(available_directions)
                destination_city = getattr(self.current_city, direction)
                self.current_city.occupants.remove(self)
                destination_city.occupants.append(self)
                self.current_city = destination_city

        def __str__(self):
            return '#' + str(self.name)


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

        @property
        def available_travel_directions(self):
            # make sure we don't return destroyed cities
            available_directions = []
            for direction in self.DIRECTIONS:
                if getattr(self, direction, None):
                    available_directions.append(direction)
            return available_directions

        @property
        def is_overcome(self):
            return len(self.occupants) >= 2

        def populate_neighbours(self, city_index):
            # associate neighbour city objects with the current city
            for direction in self.DIRECTIONS:
                direction_ref = self.refs.get(direction, None)
                if direction_ref:
                    setattr(self, direction, city_index[direction_ref])

        def get_pretty_occupants(self):
            if not len(self.occupants):
                return ''
            elif len(self.occupants) == 1:
                return str(self.occupants[0])
            str_occupants = [str(occupant) for occupant in self.occupants]
            return ', '.join(str_occupants[:-1]) + ' and ' + str_occupants[-1]

        def to_output(self):
            # generate result output based on the initial input format
            output = self.name
            for direction in self.DIRECTIONS:
                direction_ref = self.refs[direction]
                if getattr(self, direction, False) and direction_ref:
                    output += " %s=%s" % (direction, direction_ref)
            return output

        def __str__(self):
            return self.name


    def __init__(self):
        self.city_index = {}
        self.monsters = []

    def _get_world_file_data(self):
        f = open(self.DATA_FILE, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _create_city(self, line):
        # parse data from file line
        r = self.City.get_input_regex().search(line)
        city_attrs = r.groupdict()
        # init city
        city = self.City(city_attrs)
        # add city to the game index
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

    def check_game_ending_conditions(self):
        if not len(self.monsters):
            if not len(self.cities):
                print "Success! All cities have been destroyed!"
            else:
                print "All you monsters have died.Your plans for world domination have been postponed."
            return True
        return False


    def destroy_city(self, city):
        print "%s has been destroyed by monsters %s" % (city.name, city.get_pretty_occupants())
        pass

    def run(self):
        for tick in range(0, self.ROUND_LIMIT):
            if self.check_game_ending_conditions():
                return

            cities_to_destroy = filter(city_condition_filter, self.cities)
            for city in cities_to_destroy:
                self.destroy_city(city)


# Utils
def city_condition_filter(city):
    return city.is_overcome


# Main
if __name__ == '__main__':
    # argument parsing
    parser = argparse.ArgumentParser(description='Evil overlord sends monsters to eat cities')
    parser.add_argument('monsters', action="store", type=int, help="Number of monsters")
    args = parser.parse_args()

    if args.monsters < 2:
        print "You need at least 2 monsters to be able to destroy any cities."
        sys.exit()


    # Get set
    game = Game()
    game.populate_map()
    game.deploy_monsters(args.monsters)

    # GO!
    game.run()

    game.show_result()
