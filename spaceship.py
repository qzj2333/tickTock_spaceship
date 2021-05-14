import curses
import random
import time
import numpy as np

# constants that can be change
frameHeight = 20
frameWidth = 60
prob = 0.01  # percentage of obstacles on one row
speed = 200 # in ms

# initial variables
score = 0
board = []
gameEnd = False
key = 27    # ESC
# spaceship location at bottom middle
currX = frameWidth / 2
currY = frameHeight - 1
# bound inclusive
leftBound = 1   
rightBound = frameWidth - 2

# initialize game window
def initializeWindow():
    curses.initscr()
    win = curses.newwin(frameHeight, frameWidth, 0, 0) # rows, columns
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.nodelay(1)
    win.timeout(speed)
    return win

# generate one row of new obstacles based on givn probability
def generateRow(prob):
    result = []
    for i in range(frameWidth):
        if np.random.rand() > prob:
            result.append(0)
        else:
            result.append(1)
    return result


# main method
win = initializeWindow()
while not gameEnd:
    # display score
    win.addstr(0, 2, 'Score ' + str(score) + ' ')
    
    # update spaceship location
    key = win.getch()
    if key == curses.KEY_LEFT and (currX - 1) >= leftBound:
        win.addch(currY, currX, ' ')
        currX -= 1
    elif key == curses.KEY_RIGHT and (currX + 1) <= rightBound :
        win.addch(currY, currX, ' ')
        currX += 1
    # draw spaceship
    win.addch(currY, currX, '*')

    # generate new row and update board
    newRow = generateRow(prob)
    board.insert(0, newRow)
    if(len(board) > frameHeight):
        board = board[0:-1]
    
    for row in range(1, len(board)):
        for col in range(leftBound, rightBound+1):
            if board[row][col] == 1:    # current row/col is obstacle
                if(row == currY and col == currX):  # hit
                    win.addch(row, col, 'x')
                    gameEnd = True
                if row == currY - 1 and col == currX: # going to hit - change sign
                    win.addch(row, col, 'x')
                else:
                    win.addch(row, col, '-')
            else:   # current row/col is not obstacle
                if(row == currY and col == currX):  # pass one row -> update score
                    score += 1
                else:   
                    win.addch(row, col, ' ')
time.sleep(2)
curses.endwin()
