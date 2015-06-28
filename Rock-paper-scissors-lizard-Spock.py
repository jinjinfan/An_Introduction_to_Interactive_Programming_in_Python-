# Rock-paper-scissors-lizard-Spock
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random
# helper functions
# converts the string name into a number between 0 and 4
def name_to_number(name):
    number = None
    if (name == 'rock'):
        number = 0        
    elif (name == 'Spock'):
        number = 1
    elif (name == 'paper'):
        number = 2
    elif (name == 'lizard'):
        number = 3
    elif (name == 'scissors'):
        number = 4
    else:
        number = None
        print "Error:",name,"does not match any of the five correct input strings"
    return number

#converts a number in the range 0 to 4 into its corresponding name as a string
def number_to_name(number):
    name = None
    if (number == 0):
        name = 'rock'
    elif (number == 1):
        name = 'Spock'
    elif (number == 2):
        name = 'paper'
    elif (number == 3):
        name = 'lizard'
    elif (number == 4):
        name = 'scissors'
    else:
        print "Error:",number,"is not in the correct range 0 to 4"
    return name

# main function to realize Rock-paper-scissors-lizard-Spock 
def rpsls(player_choice):
    print ""
    # print the player's choice and compute player's number 
    print "Player chooses",player_choice   
    player_number = name_to_number(player_choice)
    # exit the program when player's choice is invalid
    if (player_number == None):
        exit()
    # compute random guess for comp_number and print computer's choice
    comp_number = random.randrange(0, 5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses",comp_choice
    
    # compute difference and determine winner
    comp_player_diff = (comp_number - player_number) % 5
    if (comp_player_diff == 1) or (comp_player_diff == 2):
        print "Computer wins!"
    elif (comp_player_diff == 3) or (comp_player_diff == 4):
        print "Player wins!"
    else:
        print "Player and computer tie!"
          
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
