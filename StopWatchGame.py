# template for "Stopwatch: The Game"
import lib.simpleguitk.simpleguitk as simplegui

# define global variables
TIME_INTERVAL = 100 #100 milliseconds or .1 seconds
FRAME_WIDTH = 400 #global variable to hold the width of the frame
FRAME_HEIGHT = 300 #global variable to hold the height of the frame
BUTTON_WIDTH = 200 #global variable to hold the width of the buttons

currentTime = 0 #integer representing time in tenths of seconds
timerState = False #state of the timer, false is stopped, true if running
timer = 0 #global variables to hold the timer
frame = 0 #global variable to hold the frame
totalStopCount = 0 #global variable to track total number of stops
successCount = 0 #global variable to track how many successful stops on a whole second (1.0, 2.0, etc...)




# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def calcMinutes(t):
    return int( t/600 )

def calcSeconds(t):
    return int( (t/10)%60 )

def calcCentiSeconds(t):
    return int( t%10 )

def format(t):
    numMinutes = calcMinutes(t)
    numSeconds = calcSeconds(t)
    numCentiSeconds = calcCentiSeconds(t)
    formattedTime = "%(A)01d:%(BC)02d.%(D)01d" % \
    {'A': numMinutes, 'BC': numSeconds, 'D': numCentiSeconds}
    
    return formattedTime

# define event handlers for buttons; "Start", "Stop", "Reset"
def startButtonPressed_event():
    global timer, timerState
    timer.start()
    timerState = True

def stopButtonPressed_event():
    global timer, timerState, totalStopCount, successCount, currentTime
    timer.stop()
    if timerState:
        totalStopCount += 1
        if calcCentiSeconds(currentTime) == 0 and currentTime > 0:
            successCount += 1
    
    timerState = False

def resetButtonPressed_event():
    global timer, timerState, totalStopCount, successCount, currentTime
    currentTime = 0
    totalStopCount = 0
    successCount = 0
    timer.stop()
    timerState = False


# define event handler for timer with 0.1 sec interval
def incrementTime():
    global currentTime
    currentTime += 1
#print format(currentTime) #print statement for testing
#print str(currentTime) #print statement for testing


# define draw handler
def drawHandler(canvas):
    global frame, FRAME_WIDTH, FRAME_HEIGHT, currentTime, totalStopCount, successCount
    TIME_TEXT_FONT_SIZE = 60 #size of the current time font
    TIME_TEXT_COLOR = "White"
    
    timeText = format(currentTime)
    
    timeTextWidth = frame.get_canvas_textwidth(timeText, TIME_TEXT_FONT_SIZE)
    timeTextLocation = ((FRAME_WIDTH - timeTextWidth)/2, FRAME_HEIGHT/2)
    
    canvas.draw_text(timeText, timeTextLocation, TIME_TEXT_FONT_SIZE, TIME_TEXT_COLOR)
    
    SCORE_TEXT_FONT_SIZE = 30
    SCORE_TEXT_COLOR = "Red"
    
    scoreText = "%(success)01d/%(total)01d" % \
    {'success': successCount, 'total': totalStopCount}
    
    scoreTextWidth = frame.get_canvas_textwidth(scoreText, SCORE_TEXT_FONT_SIZE)
    scoreTextLocation = ( (FRAME_WIDTH - scoreTextWidth), SCORE_TEXT_FONT_SIZE )
    
    canvas.draw_text(scoreText, scoreTextLocation, SCORE_TEXT_FONT_SIZE, SCORE_TEXT_COLOR)




# create frame
def addButtons(frame):
    global BUTTON_WIDTH
    startButton = frame.add_button('Start', startButtonPressed_event, BUTTON_WIDTH)
    stopButton = frame.add_button('Stop', stopButtonPressed_event, BUTTON_WIDTH)
    resetButton = frame.add_button('Reset', resetButtonPressed_event, BUTTON_WIDTH)
    
    return frame

def createFrame():
    global FRAME_WIDTH, FRAME_HEIGHT
    
    FRAME_NAME = 'Stopwatch - THE GAME'
    
    #create frame
    frame = simplegui.create_frame(FRAME_NAME, FRAME_WIDTH, FRAME_HEIGHT)
    
    #add buttons to frame
    frame = addButtons(frame)
    
    #register frame event handlers
    frame = setEventHandlers(frame)
    
    return frame



# register event handlers
def setEventHandlers(frame):
    frame.set_draw_handler(drawHandler)
    return frame


# start frame
def main():
    global TIME_INTERVAL, frame, timer
    #create a timer with timed event
    timer = simplegui.create_timer(TIME_INTERVAL, incrementTime)
    #create frame
    frame = createFrame()
    
    #start frame
    frame.start()

if __name__ == "__main__":
    main()
# Please remember to review the grading rubric
