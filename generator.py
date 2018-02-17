import random


# returns a with config gennerated string
def generate(config):
    out = ""
    words = config[0]
    structure = config[1]
    out += gen_str(structure, words)
    return out


# gets a random word from words[num]
def get_word(num, words):
    if num == -1:
        return ""
    collection = words[num]
    rand = random.randint(1, len(collection) - 1)
    return collection[rand] + " "


# gennerates a string out of struc
def gen_str(struc, words):
    out = ""

    if type(struc) is int:
        out += get_word(struc, words)
    else:
        for c in range(1, len(struc)):
            on = struc[c]
            if type(on) is int:
                out += get_word(on, words)
            else:
                max_percent = 0
                percent_list = []

                for i in on:
                    max_percent += i[0]
                    percent_list += [max_percent]

                rand = random.randint(1, max_percent)

                for j in range(0, len(percent_list)):
                    if percent_list[j] >= rand:
                        out += gen_str(on[j], words)
                        # print(percent_list)
                        # print(max_percent)
                        # print(j)
                        # print(rand)
                        break

    return out


# returns a list with the description and the number of a category to that things can get added
def get_addable(config):
    words = config[0]
    description = "!"
    counter = 0
    for i in words:
        if i[0].startswith("!"):
            counter += 1
    if counter == len(words):
        return ["!Error: nothing avainable", -1]
    while description.startswith("!"):
        rand = random.randint(0, len(words) - 1)
        description = words[rand][0]
    return [description, rand]


# used to add a word  to the addabele/num inside config
def add_addable(config, word, num):
    if num != -1:
        words = config[0]
        words[num] += [word]




