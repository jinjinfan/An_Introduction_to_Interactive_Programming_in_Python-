# Card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global state,list,exposed,exposed_index1,exposed_index2,turn_number
    # initialize state to 0
    state = 0
    # initialize list
    list = range(8) + range(8)
    random.shuffle(list)
    # initialize exposed list
    exposed_index1 = None
    exposed_index2 = None
    exposed = []
    for index_exposed in range(len(list)):
        exposed.append(False)
    # initialize turn number
    turn_number = 0

# define event handlers
def mouseclick(pos):
    global state,exposed_index1,exposed_index2,turn_number
    # select a card
    index_exposed = pos[0]//50
    # if select the first card
    if state == 0:
        exposed[index_exposed] = True
        exposed_index1 = index_exposed
        state = 1
        # update turn times after either the first card is flipped during a turn
        turn_number = turn_number + 1
    # if select the second card
    elif state == 1:
        # the selected card isn't exposed
        if not exposed[index_exposed]:
            # expose the card
            exposed[index_exposed] = True
            exposed_index2 = index_exposed
            state = 2
    # if select the third card
    else:
        # the selected card isn't exposed
        if not exposed[index_exposed]:
            # if the previous two exposed cards mismatch
            if list[exposed_index1] != list[exposed_index2]:
                # flip two cards back over
                exposed[exposed_index1] = False
                exposed[exposed_index2] = False
            # expose the third card
            exposed[index_exposed] = True
            exposed_index1 = index_exposed
            state = 1
            # update turn times after either the first card is flipped during a turn
            turn_number = turn_number + 1

# cards are logically 50x100 pixels in size
def draw(canvas):
    for index in range(len(list)):
        for index_exposed in range(len(exposed)):
            # display the card's value when ith entry is true
            if (exposed[index]):
                num_pos = [12 + index * 50,70]
                canvas.draw_text(str(list[index]), num_pos, 50, 'White')
            # otherwise draw a blank green rectangle
            else:
                canvas.draw_polygon([[index * 50,0], [50 + index * 50,0],\
                       [50 + index * 50,100], [index * 50,100]], 2, 'Black', 'Green')
    label.set_text('Turns = '+str(turn_number))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
