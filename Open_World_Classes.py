class Game:
    """
    The Game class is the core of a game.
    Everything is stored in side of it.
    You can have multiple Games at the same time.
    It is also made to store a game.
    """

    def __init__(self, name, server_id, world, playes):
        self.name = name
        self.server_id = server_id
        self.world = world
        self.players = playes

    # player functions
    def get_player(self, player_id):
        return self.players[player_id]

    def get_players(self):
        return self.players

    def add_player(self, player):
        self.players += [player]

    # place/world functions
    def get_place(self, place_id):
        return self.world.get_place([place_id])

    def get_world(self):
        return self.world

    # name functions
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    # game control functions
    def start_game(self):

    # TODO

    def stop_game(self):

    # TODO


class World:
    """
    The class World saves all places and has a name.
    It was made that you can save and use a world in multiple games.
    """

    def __init__(self):