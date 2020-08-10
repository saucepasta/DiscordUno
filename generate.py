import random

colors = {
    '0': 'red',
    '1': 'green',
    '2': 'yellow',
    '3': 'blue'
}

emts = {
    '0': '🔴',
    '1': '🟢',
    '2': '🟡',
    '3': '🔵'
}

actions = {
    '0': 'draw2',
    '1': 'reverse',
    '2': 'skip'
}

act = '⚫'

class Card(object):
    color = None
    value = None
    action = False
    emote = ''
    def __init__(self, color, value, action, emote):
        self.color = color
        self.value = value
        self.action = action
        self.emote = emote

    def __str__(self):
        return self.color + self.value

    def __repr__(self):
        return self.color + self.value

def generate_deck(deck):
    for i in range (0, 4):
        for j in range(0, 10):
            c = Card(colors[str(i)], str(j), False, colors[str(i)][:1] + '_' + str(j))
            if(j == 0):
                deck.append(c)
            else:
                deck.append(c)
                deck.append(c)
        for j in range(0, 3):
            c = Card(colors[str(i)], actions[str(j)], True, colors[str(i)][:1] + '_' + actions[str(j)][:1])
            deck.append(c)
            deck.append(c)
    draw = Card('', 'draw4', True, 'draw4')
    wild = Card('', 'wild', True, 'wild')
    for i in range(0, 4):
        deck.append(draw)
        deck.append(wild)
    return deck

def shuffle_deck(shuffle):
    for i in range(0, len(shuffle)):
        j = random.randint(0, len(shuffle)-1)
        temp = shuffle[i]
        shuffle[i] = shuffle[j]
        shuffle[j] = temp
    return shuffle
