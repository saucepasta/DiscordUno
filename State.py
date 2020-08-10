class State(object):
    game = None
    listening = False
    invite = ''
    embed = None
    cardMaster = None
    deck = None
    gameMessage = None
    running = False
    deckEmbed = None
    allPlayers = []
    deckMessage = None
    deckEmbed = None
    playerStats = {}
    userData = {}
    statMessage = None
    statEmbed = None
    reverse = False
    def clear(self):
        self.game = None
        self.listening = False
        self.invite = ''
        self.embed = None
        self.cardMaster = None
        self.deck = None
        self.gameMessage = None
        self.running = False
        self.deckEmbed = None
        self.allPlayers = []