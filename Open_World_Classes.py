class Game:
    """
    The Game class is the core of a game.
    Everything is stored in side of it.
    You can have multiple Games at the same time.
    It is also made to store a game.
    """

    def __init__(self, name, server_id, world, players):
        self.name = name
        self.server_id = server_id
        self.world = world
        self.players = players

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

    def to_string(self):
        return self.name

    # game control functions
    def start_game(self):  # TODO

    def stop_game(self):  # TODO


class World:
    """
    The class World saves all places and has a name.
    It was made that you can save and use a world in multiple games.
    """

    def __init__(self, name, places, commands):
        self.name = name
        self.places = places
        self.commands = commands

    # commands function
    def add_command(self, command, keys):
        self.commands += {command: keys}

    # place functions
    def get_places(self):
        return self.places

    def get_place(self, place_id):
        return self.places[place_id]

    def add_place(self, place):  # TODO

    # world handling functions
    def build_world(self):  # TODO

    def destroy_world(self):  # TODO

    # name functions
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def to_string(self):
        return self.name


class Place:
    """
    The Place class describes a place were players can go to and talk with other players at this place.
    """

    def __init__(self, name, emoji, channel_id, connections, commands, players):
        self.name = name
        self.emoji = emoji
        self.channel_id = channel_id
        self.connections = connections
        self.commands = commands
        self.players = players

    # name functions
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def to_string(self):
        return self.name

    # emoji functions
    def get_emoji(self):
        return self.emoji

    def set_emoji(self, emoji):
        self.emoji = emoji

    # channel_id functions
    def get_channel_id(self):
        return self.channel_id

    def set_channel_id(self, channel_id):
        self.channel_id = channel_id

    # connection functions
    def get_connections(self):
        return self.connections

    def set_connections(self, connections):
        self.connections = connections

    def get_connection(self, connection_id):
        return self.connections[connection_id]

    def add_connection(self, connection):
        self.connections += [connection]

    # command functions
    def get_commands(self):
        return self.commands

    def set_commands(self, commands):
        self.commands = commands

    def get_command_permission(self, command):
        return self.commands[command]

    # player functions
    def get_players(self):
        return self.players

    def player_enters(self, player_id):
        self.players += [player_id]

    def player_leaves(self, player_id):
        self.players -= [player_id]


class Connection:
    """

    """

    def __init__(self, destination, super_owner, permissions, sneakable):
        self.destination = destination
        self.super_owner = super_owner
        self.permissions = permissions
        self.sneakable = sneakable
