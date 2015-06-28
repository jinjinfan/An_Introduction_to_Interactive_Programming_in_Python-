# "Guess the number"
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code here
num_range = 100
secret_number = 0
guess_times = 0

# helper function to start and restart the game
def new_game():
    global secret_number
    global guess_times
    print ""
    print "New game. Range is from 0 to", num_range
    # set the secret number
    secret_number = random.randrange(0, num_range)
    # set the initial guess times
    guess_times = int(math.ceil(math.log(num_range + 1, 2)))
    print "Number of remaining guesses is", guess_times

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global num_range
    num_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global num_range
    num_range = 1000
    new_game()

def input_guess(guess):
    global guess_times

    # converts the string to the integer
    guess_int = int(guess)
    print ""

    # checks if the entered value is within the range
    if guess_int >= 0 and guess_int < num_range:
        print "Guess was", guess_int

        # print the remaining guesses
        guess_times = guess_times - 1
        print "Number of remaining guesses is", guess_times

        # compares the entered number to the secret number
        if guess_int == secret_number:
            print "Correct!"
            new_game()
        elif guess_times == 0:
            print "You ran out of guesses. The number was",secret_number
            new_game()
        elif guess_int < secret_number:
            print "Higher!"
        else:
            print "Lower!"
    else:
        print "Error:The entered number", guess_int,"is not in the range [0,",num_range,")"

# create frame
frame = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements and start frame
frame.add_button('Range is [0, 100)', range100, 200)
frame.add_button('Range is [0, 1000)', range1000, 200)
frame.add_input('Enter a guess', input_guess, 200)

# call new_game
new_game()
