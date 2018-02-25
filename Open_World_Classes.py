class Game:
    """
    The Game class is the core of a game.
    Everything is stored in side of it.
    You can have multiple Games at the same time.
    It is also made to store a game.
    """

    def __init__(self, name, server_id, world, players, client):
        self.name = name
        self.server_id = server_id
        self.world = world
        self.players = players
        self.client = client

    # client functions
    def get_client(self):
        return self.client

    def set_client(self, client):
        self.client = client

    # player functions
    def get_player(self, player_id):
        return self.players[player_id]

    def get_players(self):
        return self.players

    def add_player(self, player):
        self.players += {player.get_discord_id():player}

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
        print("TODO")
    def stop_game(self):  # TODO
        print("TODO")

class World:
    """
    The class World saves all places and has a name.
    It was made that you can save and use a world in multiple games.
    """

    def __init__(self, game, name, places, commands):
        self.game = game
        self.name = name
        self.places = places
        self.commands = commands

    # commands function
    def add_command(self, command, keys):
        self.commands += {command: keys}

    def get_command_permissions(self, command):
        return self.commands[command]

    # place functions
    def get_places(self):
        return self.places

    def get_place(self, place_id):
        return self.places[place_id]

    def add_place(self, place):  # TODO
        print("TODO")
    # world handling functions
    def build_world(self):  # TODO
        print("TODO")
    def destroy_world(self):  # TODO
        print("TODO")
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

    def __init__(self, game, name, emoji, channel_id, connections, commands, players):
        self.game = game
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

    def get_command_permissions(self, command):
        return self.commands[command]

    # player functions
    def get_players(self):
        return self.players

    def player_enters(self, player_id):
        self.players += [player_id]

    def player_leaves(self, player_id):
        self.players -= [player_id]

    def send_message(self, player, message):
        string = player.get_emoji() + player.get_nickname() + ": " + "message"
        for p in self.players:
            if p != player:
                self.game.get_player(p).send_message(string)


class Connection:
    """
    This class represents the connection between the places.
    It say who can travel where and how.
    """

    def __init__(self, game, destination, super_owner, permissions, sneakable):
        self.game = game
        self.destination = destination
        self.super_owner = super_owner
        self.permissions = permissions
        self.sneakable = sneakable

    # destination functions
    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    # permission functions
    def get_super_owner(self):
        return self.super_owner

    def set_super_owner(self, super_owner):
        self.super_owner = super_owner

    def get_permissions(self):
        return self.permissions

    def set_permissions(self, permissions):
        self.permissions = permissions

    # sneakable functions
    def get_sneakable(self):
        return self.sneakable

    def set_sneakable(self, sneakable):
        self.sneakable = sneakable


class Player:
    """
    The Player class represents a Player with all his attributes and rights.
    """

    def __init__(self, game, discord_id, channel_id, nickname, emoji, place, keys):
        self.game = game
        self.discord_id = discord_id
        self.channel_id = channel_id
        self.nickname = nickname
        self.emoji = emoji
        self.place = place
        self.keys = keys

    # discord_id functions
    def get_discord_id(self):
        return self.discord_id

    def set_discord_id(self, discord_id):
        self.discord_id = discord_id

    # channel_id functions
    def get_channel_id(self):
        return self.channel_id

    def set_channel_id(self, channel_id):
        self.channel_id = channel_id

    # nickname functions
    def get_nickname(self):
        return self.nickname

    def set_nickname(self, nickname):
        self.nickname = nickname

    # emoji functions
    def get_emoji(self):
        return self.emoji

    def set_emoji(self, emoji):
        self.emoji = emoji

    # place functions
    def get_place(self):
        return self.place

    def set_place(self, place):
        self.place = place

    # key functions
    def get_keys(self):
        return self.keys

    def set_keys(self, keys):
        self.keys = keys

    def add_key(self, key):
        self.keys += key

    def delete_key(self, key):
        self.keys -= key

    # message functions
    def on_message(self, message):
        if message.startswith("."):
            arguments = message.split()
            if self.game.get_world().get_command_permissions(arguments[0][1:]) in self.keys:
                print("TODO")
            # exectue command //TODO
            elif self.game.get_place(self.place).get_command_permissions(arguments[0][1:]) in self.keys:
                print("TODO")
            # exectue command //TODO
            else:
                print("TODO")
        # send back "no permission"
        elif not message.startswith("%"):
            self.game.get_place(self.place).send_message(self,message)

