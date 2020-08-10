class Uno(object):
    gameChannel = None
    playerCount = 0
    cardMaster = None
    gameQueue = []
    totalCards = 0
    currentPlayer = None
    currentIndex = 0
    topCard = None
    cardStack = []
    def __init__(self, cardMaster, gameQueue, totalCards, gameChannel):
        self.cardMaster = cardMaster
        self.gameQueue = gameQueue
        self.totalCards = totalCards
        self.gameChannel = gameChannel