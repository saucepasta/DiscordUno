class Player(object):
    deck = []
    user = ''
    turns = 0
    dm = None
    def __init__(self, user, deck):
        self.deck = deck
        self.user = user