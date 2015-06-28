# "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
# the total number of stops
number_stops = 0
# the number of successful stops at a whole second
nmber_win = 0
# determine whether stopwatch is running
timer_running = False
    
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minute = t // 600
    second = (t % 600 ) // 10
    second_tenth = t - minute * 600 - second * 10
    if second < 10:
        str_sec = "0" + str(second)
    else:
        str_sec = str(second)        
    return str(minute) + ":" + str_sec + "." + str(second_tenth)      

# display the game results
def game_result():
    return str(nmber_win) + " / " + str(number_stops)
        
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer_running
    # set the variable to True when running the timer
    timer_running = True
    timer.start()
    
def stop():
    global number_stops
    global nmber_win
    global timer_running
    if timer_running == True:
        # add the total number of stops by 1 
        number_stops = number_stops + 1
        # when successfully stops at a whole second
        if time % 10 == 0:
            # add the win number by 1
            nmber_win = nmber_win + 1 
        # set the variable to False when the stopwatch stops
        timer_running = False    
    timer.stop()
       
def reset():
    global time
    global number_stops
    global nmber_win
    global timer_running
    time = 0
    number_stops = 0
    nmber_win = 0
    timer_running = False

# define event handler for timer with 0.1 sec interval
def timer():
    global time
    time = time + 1
    
# define draw handler
def display(canvas):
    canvas.draw_text(format(time), (50, 90), 40, 'White')
    canvas.draw_text("win / total",(135, 20),15,'Red')
    canvas.draw_text(game_result(), (140, 40), 23, 'Red')
    
# create frame
frame = simplegui.create_frame("Stop watch", 200, 150)
label = frame.add_label("Stopwatch: The Game")

# register event handlers
frame.add_button("Start", start, 120)
frame.add_button("Stop", stop, 120)
frame.add_button("Reset", reset, 120)
frame.set_draw_handler(display)
timer = simplegui.create_timer(100, timer)

# start frame
frame.start()

