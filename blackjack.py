# Blackjack
"""
Redegine betting/scoring system for Blackjack

Giving a betting system, by default the money you want to bet
is 10, when you win, you can get doubled money added to your
account; otherwise, just betting money substracted.

In addition, you can bet the amount of money you like.

"""
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

BACKGROUND_SIZE = [1288, 716]
BACKGROUND_CENTER = [644, 358]
background_image = simplegui.load_image("http://solaireresort.com/cms/wp-content/uploads/2014/01/Blackjack1288x716-1288x716.jpg")

# initialize some useful global variables
in_play = False
outcome = ""
outcome_new = ""
first_enter = True
money = 100
betting_money = 10

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# helper function
def game_end(status):
    global money, betting_money, in_play, first_enter
    global outcome_new
    # if you win
    if status:
        money = money + betting_money * 2
    else:
        money = money - betting_money
    # initialize not in the game
    in_play = False
    # set first entered betting as true
    first_enter = True
    outcome_new = "New deal?"

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        hand_str = "Hand contains: "
        for hand_index in range(len(self.hand)):
            hand_str += str(self.hand[hand_index]) + " "
        return hand_str

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        hand_value = 0
        ace_in = False
        for hand_index in range(len(self.hand)):
            # when card has an 'A'
            if self.hand[hand_index].rank == 'A':
                ace_in = True
            hand_value += VALUES[self.hand[hand_index].rank]
        # when the value plus 10 not greater than 21
        if ace_in and hand_value + 10 <= 21:
            hand_value = hand_value + 10
        return hand_value

    def draw(self, canvas, pos):
        for hand_index in range(len(self.hand)):
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.hand[hand_index].rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.hand[hand_index].suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE,
                              [pos[0] + CARD_CENTER[0]+CARD_SIZE[0]*hand_index, pos[1] + CARD_CENTER[1]], CARD_SIZE)

    def draw_back(self, canvas, pos):
        #pos_list = [[CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]],[CARD_BACK_CENTER[0]+CARD_BACK_SIZE, CARD_BACK_CENTER[1]]]
        card_back_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for j in range(len(SUITS)):
            for i in range(len(RANKS)):
                self.deck.append(Card(SUITS[j], RANKS[i]))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def __str__(self):
        deck_str = "Deck contains: "
        for deck_index in range(len(self.deck)):
            deck_str += str(self.deck[deck_index]) + " "
        return deck_str

#define event handlers for buttons
def deal():
    global outcome, in_play, outcome_new
    global deck,hand_player,hand_dealer
    outcome = "Hit or stand?"
    outcome_new = ""
    # if not in play when hitting the Deal button
    if not in_play:
        in_play = True
        # shuffle the deck
        deck = Deck()
        deck.shuffle()

        # create two hands for player and dealer
        hand_player = Hand()
        hand_player.add_card(deck.deal_card())
        hand_player.add_card(deck.deal_card())

        hand_dealer = Hand()
        hand_dealer.add_card(deck.deal_card())
        hand_dealer.add_card(deck.deal_card())

    else:
        outcome = "You lose"
        game_end(False)

def hit():
    global outcome, in_play, first_enter
    global hand_player
    # if the hand is in play, hit the player
    if in_play:
        first_enter = False
        hand_player.add_card(deck.deal_card())
        # if busted
        if hand_player.get_value() > 21:
            #assign a message to outcome
            outcome = "You busted"
            game_end(False)

def stand():
    global outcome, in_play
    global hand_dealer
    # if the hand is in play, hit the player
    if in_play:
        #repeatedly hit dealer until his hand has value 17 or more
        while hand_dealer.get_value() < 17:
            hand_dealer.add_card(deck.deal_card())
        # if no busted or dealer's hand value is not less than the player's
        if 21 >= hand_dealer.get_value() >= hand_player.get_value():
            outcome = "You lose"
            game_end(False)
        else:
            outcome = "You win"
            game_end(True)

# input handler
def betting(text_input):
    global betting_money, outcome_new
    global first_enter, in_play
    # if first enter the betting
    if first_enter:
        if 20 >= int(text_input) >= 5 :
            # change first entered flag to false
            first_enter = False
            betting_money = int(text_input)
            outcome_new = ""

        else:
            outcome_new = "Invalid betting!Between 5 and 20!"
    else:
         outcome_new = "Betting modified in the game!"

# draw handler
def draw(canvas):
    global outcome,outcome_new
    # draw background
    canvas.draw_image(background_image, BACKGROUND_CENTER, BACKGROUND_SIZE, (300, 300), (600, 600))

    # draw the hand
    hand_dealer.draw(canvas,[50,200])
    hand_player.draw(canvas,[50,300])
    # if in play, draw an image of the back of a card over dealer's first card
    if in_play == True:
       hand_dealer.draw_back(canvas,[50,200])

    #draw the message
    canvas.draw_text(outcome, (20, 500), 25, 'White')
    canvas.draw_text(outcome_new, (20, 550), 25, 'White')

    # draw game title
    canvas.draw_text("Blackjack", (425, 60), 40, 'Green')

    # draw money
    canvas.draw_text("Money: "+str(money), (450, 100), 25, 'Blue')

    # draw betting money per round
    label.set_text('Betting Money = '+str(betting_money))

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
label = frame.add_label("Betting Money = 10")
frame.add_input('Enter between 5 and 20 per round',betting, 150)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
