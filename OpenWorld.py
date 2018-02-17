# import pip
# pip.main(['install', "discord.py"])
import discord
import asyncio
import json

client = discord.Client()


def setup():
    global gl_users
    global gl_receiver_list
    global gl_places
    global gl_place_name
    gl_place_name = ""
    global gl_info
    gl_info = False
    global gl_change_location
    gl_change_location = False

    def user_load():  # Load userdata
        global gl_users
        try:
            with open("user.json", "r") as file:
                gl_users = json.loads(file.read())
        except:
            print("Keine Benutzerdatenbank gefunden. Benutzerdatenbank wird erstellt.")
            with open("user.json", "w") as file:
                gl_users = {}

    user_load()

    def world_load():  # load worlddata
        global gl_places
        try:
            with open("world.json", "r") as file:
                gl_places = json.loads(file.read())
        except:
            print("Keine Weltdatenbank gefunden. Weltdatenbank wird erstellt.")
            with open("world.json", "w") as file:
                gl_places = {}

    world_load()
    global gl_receiver
    global gl_content
    gl_receiver = client.user
    gl_content = ""


@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    setup()


@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
    if str(user.id) != client.user.id:
        global gl_places
        for location in gl_places:
            if reaction.emoji == gl_places[location][0]["emoji"]:
                yield from change_location(user, [".changeLocation", location])
                yield from client.delete_message(reaction.message)


@client.event
@asyncio.coroutine
def on_message(message):
    global gl_places
    print(str(message.author) + " : " + message.content)
    if str(message.author.id) != client.user.id and message.server is None:  # if author is not the Bot
        bol_command = yield from commands(message.author, message.channel, message.content, message.timestamp, "d")
        #print("Command is executed: " + str(bol_command))
        if not bol_command and not message.content.startswith("%"):
            content = user_nickname(message.author) + ": " + message.content
            log_channel = gl_places[user_place(message.author)][0]["channel_id"]
            log_channel = discord.Object(log_channel)
            yield from send_message(log_channel, content)
            yield from client.add_reaction(message, "📲")  # send reaction to sender
            yield from send_multiple_message(place_user(user_place(message.author)), message.author.id, content)



@asyncio.coroutine
def send_message(receiver, content):
    message = yield from client.send_message(receiver, content)
    return message


@asyncio.coroutine
def send_multiple_message(receiver_list, exception, content):
    for receiver in receiver_list:
        if exception == receiver:
            continue
        try:
            receiver = yield from client.get_user_info(receiver)
        except:  # If user is channel
            receiver = discord.Object(receiver)
        yield from send_message(receiver, content)


@asyncio.coroutine
def add_multiple_reactions(message, emojis):
    for emoji in emojis:
        yield from client.add_reaction(message, emoji)


@asyncio.coroutine
def commands(author, channel, content, timestamp, app):
    global gl_users
    global gl_receiver
    global gl_content
    global gl_place_name
    global gl_change_location
    # Commands
    if content.startswith(".register"):
        yield from register(author, channel, app)
        return True
    if content.startswith(".addPlace") or content.startswith(".addplace"):
        arguments = content.split()
        yield from add_place(author, channel, channel.server, arguments)
        return True
    if content.startswith(".changeLocation") or content.startswith(".changelocation") or content.startswith(".cl")or content.startswith(".cL"):
        arguments = content.split()
        yield from change_location(author, arguments)
        return True
    if content.startswith(".info") or content.startswith(".i"):
        yield from info(author, channel)
        return True
    return False


@asyncio.coroutine
def add_place(author, answer_channel, server, arguments):
    global gl_places
    place_name = arguments[1]
    travel_locations = arguments[2]
    hear_locations = arguments[3]
    command_list = arguments[4]
    emoji = arguments[5]

    if place_name in gl_places:
        content = author.mention + " This place already exists!"
        yield from send_message(answer_channel, content)
    else:
        try:
            place_channel = yield from client.create_channel(server, place_name)
            gl_places[place_name] = [
                {"name": place_name, "travel_locations": json.loads(travel_locations),
                 "hear_locations": json.loads(hear_locations), "commands": json.loads(command_list),
                 "user": [], "channel_id": place_channel.id, "emoji": emoji}]
            dump_array("world.json", gl_places)
            content = author.mention + " " + place_name + " added successfully."
        except:  # if user is not on a server
            content = author.mention + "Please execute this command on a server!"
        yield from send_message(answer_channel, content)


@asyncio.coroutine
def change_location(user, arguments):
    global gl_places
    global gl_users
    destination = arguments[1]

    for place in gl_places[user_place(user)][0]["travel_locations"]:  # Can user travel to his destination?
        if place == destination or gl_places[place][0]["emoji"] == destination:  # place name or emoji
            try:
                gl_places[user_place(user)][0]["user"].remove(user.id)  # remove user from current location
            except:
                print("")
            content = "***" + user_nickname(user) + " has arrived at " + place + "***"
            yield from send_multiple_message(place_user(place), user.id, content)
            gl_places[place][0]["user"].append(user.id)  # add user to new location
            gl_users[user.id][0]["place"] = place  # change place in userdata
            content = "```Welcome to " + place + "! Type \".info\" for info```"
            yield from send_message(user, content)
            dump_array("world.json", gl_places)
            dump_array("user.json", gl_users)
            return
    # if user cant travel:
    content = "You can not travel to " + destination + ". Type .info to get information about your current location."
    yield from send_message(user, content)


@asyncio.coroutine
def info(user, receiver):
    global gl_users
    global gl_places
    emojis = []

    content = "You are in **" + user_place(user) + "**. \n From here you can travel to these places:\n"
    # print(gl_places[user_place])
    for location in gl_places[user_place(user)][0]["travel_locations"]:
        emoji = gl_places[location][0]["emoji"]
        emojis.append(emoji)
        content = content + "-" + emoji + location + "\n"
    content = content + "\n From here you can execute this commands:\n"
    for command in gl_places[user_place(user)][0]["commands"]:
        content = content + "" + command + "\n"
    message = yield from send_message(receiver, content)
    yield from add_multiple_reactions(message, emojis)


@asyncio.coroutine
def register(user, channel, app):
    global gl_users
    global gl_places
    for cur_user in gl_users:  # Userdatenbank durchsuchen
        #print(user)
        if user.id == cur_user:
            if gl_users[user.id][0]["app"] == app:
                content = user.mention + " You have already registered. Look in your direct messages!"
                yield from send_message(channel, content)
                return
    gl_users[user.id] = [{"name": user.name, "discriminator": user.discriminator, "app": app,
                              "nickname": nickname(user), "place": "the-market"}]
    gl_places["the-market"][0]["user"].append(user.id)
    dump_array("world.json", gl_places)
    dump_array("user.json", gl_users)
    content = user.mention + " You signed in successfully! \n" + "You are now **" + gl_users[user.id][0]["nickname"] + "**"
    yield from send_message(channel, content)
    yield from send_message(user, "Welcome to the Open World Game! Type .info")


def nickname(user):
    conf = [
        [
            ["pre", "the", "Dr", "old"],
            ["evil adjectives", "evil", "angry"],
            ["good adjectives", "good", "great", "glorious"],
            ["first name", "Tim", "Tom", "Ben", "Jac", "Mike", "Chad", "Rohn", "Henry", "Frank", "Greg", "Joe",
             "Andrew",
             "Donald", "Noha", "Nathan", "John", "Robert", "Leo", "Thomas", "James", "Logan", "Archie", "Theo", "Henry",
             "Max", "Joshua", "William", "Lucas", "Ethan", "Mason", "Harrison", "Isaac", "Finley", "Teddy", "Alexander",
             "Riley", "Arthur", "Daniel", "Joseph", "Adam", "Edward", "Samuel", "Reggie", "Benjamin", "Sebastian",
             "Dylan",
             "Jaxon", "Jake", "Toby", "Harley", "Elijah", "Jenson", "Carter", "Arlo", "Louie", "Lewis", "Tommy", "Jude",
             "Hugo", "Ollie", "David", "Rory", "Alex", "Bobby", "Frankie", "Ronnie", "Jackson", "Matthew", "Zachary",
             "Harvey", "Jayden", "Luca", "Blake", "Nathan", "Elliot", "Albie", "Caleb", "Reuben", "Hunter", "Luke",
             "Tyler",
             "Stanley", "Michael", "Dexter", "Theodore", "Roman", "Ryan", "Albert", "Elliott", "Ellis", "Kai", "Louis",
             "Liam", "Finn", "Connor", "Austin", "Ezra", "Aiden", "Jamie", "Callum", "Leon", "Aaron", "Finlay",
             "Gabriel",
             "Eli", "Ben", "Grayson"],
            ["second name", "Wolf", "Smith", "Miller", "Jones", "Williams", "Taylor", "Davies", "Rubik", "Brown",
             "Wilson",
             "Evans", "Thomas", "Johnson", "Trump", "Roberts", "Walker", "Wright", "Robinson", "Thompson", "White",
             "Hughes", "Edwards", "Green", "Lewis", "Wood", "Harris", "Martin", "Jackson", "Clarke", "Chips", "Hatman",
             "Temples", "Raynott", "Woodbead", "Nithercott", "Rummage", "Southwark", "Harred", "Jarsdel"],
            ["!aristocratics", "von", "van", "from"],
            ["citys", "london", "verdict village", "new castell"]
        ],
        [
            1, [[5, -1], [1, 0]], [[7, -1], [3, 1], [5, 2]], 3, [[10, 4], [1, 5, 6]]
        ]
    ]
    import generator
    return generator.generate(conf)


def dump_array(file, array):
    with open(file, "w") as file:
        file.write(json.dumps(array))


def user_place(user):
    global gl_users
    place = gl_users[user.id][0]["place"]
    return place


def place_user(place):
    global gl_places
    users = gl_places[place][0]["user"]
    return users


def user_nickname(user):
    global gl_users
    nickname = gl_users[user.id][0]["nickname"]
    return nickname


with open("BotToken.txt", "r") as file:
    token = file.read()
client.run(token)

