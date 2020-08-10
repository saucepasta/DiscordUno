import discord
import hashlib
import generate
import random
import State
import Uno
import Player

print('Starting Up...')
client = discord.Client()

state = State.State()
tick = discord.PartialEmoji(name='✅')
all_emojis = {}

actions = {
    'D2': 'draw2',
    'D4': 'draw4',
    'WLD': 'wild',
    'RVR': 'reverse',
    'SKP': 'skip'
}


async def initialize(channel, cardMaster, message):
    unshuf = []
    state.game = Uno.Uno(cardMaster=cardMaster, gameQueue=[], totalCards=108, gameChannel=channel)
    state.deck = generate.shuffle_deck(generate.generate_deck(unshuf).copy())
    state.embed.description = '``' + cardMaster.name + '`` must type ``start ' + state.invite + '`` to start the game.\n' + state.embed.description
    await state.gameMessage.edit(embed=state.embed)

async def addPlayer(player):
    td = []
    for i in range(0, 7):
        card = random.choice(state.deck)
        td.append(card)
        state.deck.remove(card)
    state.playerStats[player.id] = 7
    state.userData[player.id] = player.name
    state.embed.description +=  '\n' + player.name + ' has joined the game.'
    state.game.playerCount += 1
    state.game.gameQueue.append(Player.Player(player, td))
    await state.gameMessage.edit(embed=state.embed)
    print(player.name + ' -> ')
    print(td)
    state.allPlayers.append(player)
    print(state.allPlayers)

async def DMDeck(user, deck):
    dm = await user.create_dm()
    i = 0
    embed = discord.Embed()
    embed.set_author(name='Your Deck: ', icon_url=user.avatar_url)
    embed.description  = '[Tap Here to go back to the game!]('+state.deckMessage.jump_url + ')\n if you can\'t use any of these cards, type ``nada`` to pick one up from the deck.'
    for card in deck:
        embed.add_field(name=all_emojis[card.emote], value=  '``' + str(i) + '``: ' + card.color + ' ' + ' ' + card.value )
        i += 1
    await dm.send(embed=embed)

async def statUpdate():
    d = 'Players\' Cards:\n'
    for i in state.playerStats:
        if i == state.game.currentPlayer.user.id:
            d += '`` > ' + str(state.userData[i]) + '``: ' + str(state.playerStats[i]) + '\n'
        else:
            d += '``   ' + str(state.userData[i]) + '``: ' + str(state.playerStats[i]) + '\n'
    state.statEmbed.description = d
    await state.statMessage.edit(embed=state.statEmbed)


async def run():
    em = discord.Embed()
    em.set_author(name= 'UNO!')
    state.game.currentPlayer = state.game.gameQueue[state.game.currentIndex]
    i = 0
    while state.deck[i].action:
        i += 1
    state.game.topCard = state.deck.pop(i)
    em.description = 'Current Card: ' + str(state.game.topCard.color) + ': ' + str(state.game.topCard.value) + '\n' + state.game.currentPlayer.user.name + '\'s turn'
    em.set_image(url='https://cdn.discordapp.com/emojis/' + str(all_emojis[state.game.topCard.emote].id) + '.png')
    em.set_footer(text='UNO® is a registered trademark of Mattel, Inc.')
    dMeck = await state.game.gameChannel.send(embed=em)
    em2 = discord.Embed()
    em2.set_author(name='Game Stats')
    d = 'Players\' Cards:\n'
    for i in state.playerStats:
        d += '``' + str(state.userData[i]) + '``: ' + str(state.playerStats[i]) + '\n'
    em2.description = d
    state.statEmbed = em2
    statM = await state.game.gameChannel.send(embed=em2)
    state.statMessage = statM
    state.deckEmbed = em
    state.deckMessage = dMeck
    await DMDeck(state.game.currentPlayer.user, state.game.currentPlayer.deck)

async def editCards(num):
    state.playerStats[state.game.currentPlayer.user.id] += num
    await statUpdate()
    for i in range(0, num):
        state.game.gameQueue[state.game.currentIndex].deck.append(state.deck.pop())
    state.game.currentPlayer = state.game.gameQueue[state.game.currentIndex]

async def nextPlayer():
    if state.reverse:
        state.game.currentIndex -= 1
        if state.game.currentIndex <= 0:
            state.game.currentIndex = len(state.game.gameQueue) - 1
        state.game.currentPlayer = state.game.gameQueue[state.game.currentIndex]
    if not state.reverse:
        state.game.currentIndex += 1
        if state.game.currentIndex >= len(state.game.gameQueue):
            state.game.currentIndex = 0
        state.game.currentPlayer = state.game.gameQueue[state.game.currentIndex]



async def handleActionCard(card, currentUser):
    if card.value == actions['D2']:
        await editCards(2)
    elif card.value == actions['D4']:
        await editCards(4)
    elif card.value == actions['SKP']:
        state.deckEmbed.description =  'a skip card was used. Skipping ' + state.game.currentPlayer.user.name
        await nextPlayer()
        state.deckEmbed.description += '\n' + state.game.currentPlayer.user.name + '\'s turn.'
        state.deckEmbed.set_image(url='https://cdn.discordapp.com/emojis/' + str(all_emojis[card.emote].id) + '.png')
        await state.deckMessage.edit(embed=state.deckEmbed)
        await statUpdate()
    elif card.value == actions['RVR']:
        state.reverse = True
        await statUpdate()



async def editDeck(player, card, dm, nocard):
    if(nocard):
        state.deckEmbed.description = player.name + ' picked up a card from the deck.\nThe current card is: ' + str(card) + '\n' + state.game.currentPlayer.user.name + '\'s turn.'
    else:
        state.deckEmbed.description = player.name + ' has used a ' + str(card) + '\n' + state.game.currentPlayer.user.name + '\'s turn.'
    state.deckEmbed.set_image(url='https://cdn.discordapp.com/emojis/' + str(all_emojis[card.emote].id) + '.png')
    await dm.add_reaction(tick)
    await state.deckMessage.edit(embed=state.deckEmbed)

def validateCards(card1, card2):
    if card1.color == card2.color:
        return True
    if card1.value == card2.value:
        return True
    elif card1.color == '':
        return True
    else:
        return False

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    # get all emojis from the emote servers for all of the cards.
    # these IDs can also be used as images with the emoji url (discord/id.png)
    bga = await client.fetch_guild(568822288431185930)
    ry = await client.fetch_guild(720629316102258728)
    emotes = bga.emojis + ry.emojis
    for emote in emotes:
        all_emojis[emote.name] = emote



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.TextChannel):
        if message.content == 'pp':
            if state.running:
                await message.channel.send(state.cardMaster.name + 's\' game' + '[ID:' + state.invite + '] is already running. Wait for it to end.')
                return
            m = hashlib.md5(str(message.id).encode('utf-8')).hexdigest()[:5]
            embed = discord.Embed()
            embed.set_author(name='Waiting For Players', icon_url='https://media.discordapp.net/attachments/568822288431185932/720352459977130044/10.gif')
            embed.description = 'I\'ve created a new game!\nType ``join ' + m + '`` to join the game.\n\n━━━━━━━━━'
            embed.set_footer(text='UNO® is a registered trademark of Mattel, Inc.')
            confirm = await message.channel.send(embed=embed)
            state.gameMessage = confirm
            state.listening = True
            state.embed = embed
            state.invite = m
            state.cardMaster = message.author
            state.running = True
            await initialize(message.channel, message.author, confirm)
            await addPlayer(message.author)

        if state.listening and message.content == 'join ' + state.invite and message.author != state.cardMaster:
            await addPlayer(message.author)

        if state.listening and message.content == 'start ' + state.invite and message.author == state.cardMaster:
            state.embed.set_author(name='Done. 3..2..1..', icon_url='https://media.discordapp.net/attachments/568822288431185932/720361459099369497/success.png')
            state.embed.description = '~~' + state.embed.description + '~~'
            await state.gameMessage.edit(embed=state.embed)
            state.listening = False
            await run()

        if state.running and message.content == 'end ' + state.invite and message.author == state.cardMaster:
            state.embed.set_author(name='Game ' + state.invite, icon_url='https://media.discordapp.net/attachments/568822288431185932/720361459099369497/success.png')
            state.embed.description = 'The Game Has Ended.'
            await state.game.gameChannel.send(embed=state.embed)
            state.clear()

    if isinstance(message.channel, discord.DMChannel):
        if state.running:
            card = None
            if state.game.currentPlayer.user == message.author:
                # if the player has no cards, let them pick one up from the deck
                if message.content == 'nada':
                    drawCard = state.deck.pop()
                    state.game.currentPlayer.deck.append(drawCard)
                    print(state.game.currentPlayer.deck)
                    # move the queue forward
                    await nextPlayer()
                    await DMDeck(state.game.currentPlayer.user, state.game.currentPlayer.deck)
                    await editDeck(message.author, state.game.topCard, message, True)
                    state.playerStats[message.author.id] += 1
                    await statUpdate()
                    return
                try:
                    # get user's message to pick a card
                    card = state.game.currentPlayer.deck[int(message.content)]
                    # card validation: check if the colors match
                    if validateCards(card, state.game.topCard):
                        pass
                    else:
                        # terminate if the card isn't valid and wait for the next input
                        await message.channel.send('Oops! You can\'t use that card. The current card is a ' + state.game.topCard.color + ' and you used a ' + card.color + '.')
                        await message.channel.send('If you don\'t have a usable card, type ``nada`` to borrow one from the deck.')
                        return
                    #checking for action cards

                except:
                    await message.channel.send('Looks like you\'re confused. Either send ``ONE`` number from the deck message above or send ``nada`` to pick a new card.')
                    return
                # if the card passes all checks, move the player queue forward and change the current player to the message author.
                state.game.currentPlayer.deck.remove(card)
                await nextPlayer()
                if card.action:
                        await handleActionCard(card, message.author)
                # DM the new deck to the next player and edit the game message in the server.
                await DMDeck(state.game.currentPlayer.user, state.game.currentPlayer.deck)
                state.game.topCard = card
                state.playerStats[message.author.id] -= 1
                await statUpdate()
                await editDeck(message.author, card, message, False)
            else:
                # if any other non-player sends a stray message: warn and ignore
                if message.author not in state.allPlayers:
                    await message.channel.send('You haven\'t joined a game yet. :(')
                if message.author in state.allPlayers:
                    await message.channel.send('Nope, Wait for your turn.')
        else:
            await message.channel.send("Bitch you didn't start a game yet")


client.run('')