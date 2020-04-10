# I liked to play 2048 game, and this is the code to achieve 2048 on your pc
# Yuanfeng Li
# 2019.7
# the website of original game: http://2048game.com/

#!/usr/bin/env python3p
# -*- coding:utf-8 -*-

"""2048 game
This module will implement the algorithm of 2048 game, and the algorithm of scores.
The game interface will use the standard library of Python - tkinter to achieve
The interface will use grid to layout.
"""


import random  # import random, to create the random number and its location
import math  # import math, to count scores

# _map_data is a matrix of 4 x 4, and it will be the map of 2048 game,
# below are default values
_map_data = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# -------------------------below are the basic algorithm for game 2048---------------------------


def reset():
    '''Reset the game data, restore the map to default state, adds two 2's to the original map'''
    _map_data[:] = []  # _map_data.clear()
    _map_data.append([0, 0, 0, 0])
    _map_data.append([0, 0, 0, 0])
    _map_data.append([0, 0, 0, 0])
    _map_data.append([0, 0, 0, 0])
    # fill two 2s on the map
    fill2()
    fill2()


def get_space_count():
    # count squares that has no 2, 4, 0, 8 s, if the count is 0, then it means there is no more 
    # for new number, and then game over.
    count = 0
    for r in _map_data:
        count += r.count(0)
    return count


def get_score():
    ''' get the score, the rule is sum of two numbers,
    such as: 2 + 2 = 4, 8 + 8 = 16.
    we can know how many times a number added to other numbers,
    such as:
        4 ---- 2 + 2 score: 4
        8 ---- 4 + 4 score: 8
        ... so on so forth
    '''
    score = 0
    for r in _map_data:
        for c in r:
            score += 0 if c < 4 else c * int((math.log(c, 2) - 1.0))
    return score  # import the math package


def fill2():
    '''fill 2 in the empty space, if success then return True, else return False'''
    blank_count = get_space_count()  # get the number of empty space on map
    if 0 == blank_count:
        return False
    # choose space randomly, when there are only 4 empty spaces, then we generate
    # 0 ~ 3, to represent the spaces from left to right, and from top to bottom. 
    pos = random.randrange(0, blank_count)
    offset = 0
    for row in _map_data:   # row: is the row on map 
        for col in range(4):  # col: is the column
            if 0 == row[col]:
                if offset == pos:
                    # fill a 2 in 'row' row, col column, and return True
                    row[col] = 2
                    return True
                offset += 1


def is_gameover():
    """ to see if game is over, if over return True, else return False
    """
    for r in _map_data:
        # if there is 0 in rows, then game is not over.
        if r.count(0):
            return False
        # if there are two adjacent identical element, then they might be able to combine,
        # which means the game is not over.
        for i in range(3):
            if r[i] == r[i + 1]:
                return False
    for c in range(4):
        # if there are two adjacent identical element vertically, then they might be able 
        # to combine, then game is not over.
        for r in range(3):
            if _map_data[r][c] == _map_data[r + 1][c]:
                return False
    # did not meet any above spec, then game is over.
    return True

# below is the basic algorithm method, it is not the best/most efficient algoritm method
# but it works really well, and it is easy to understand.


def _left_move_number(line):
    '''move all numbers in a row, if they moves return True, else return False:
    e.g.: line = [0, 2, 0, 8]:
        +---+---+---+---+
        | 0 | 2 | 0 | 8 |      <----move to left (it is default to move 1 square/ button)
        +---+---+---+---+
    this row need to move 3 times:
      the result of 1st move:
        +---+---+---+---+
        | 2 | 0 | 8 | 0 |
        +---+---+---+---+
      2nd move:
        +---+---+---+---+
        | 2 | 8 | 0 | 0 |
        +---+---+---+---+
      3rd move:
        +---+---+---+---+
        | 2 | 8 | 0 | 0 |  # because the left end of row is 2 so 8 is not moving agian
        +---+---+---+---+
     final result: line = [2, 8, 0, 0]
    '''
    moveflag = False  # the marks of whether it is moved or not, False by default
    for _ in range(3):  # repeat following algorithm 3 times
        for i in range(3):  # i is the index
            # it is empty here, the right adjacent number move to left, the right become blank 
            if 0 == line[i]: 
                moveflag = True
                line[i] = line[i + 1]
                line[i + 1] = 0
    return moveflag


def _left_merge_number(line):
    '''move the row to left, combine cells, put result on left, 0 on right
    e.g.: line = [2, 2, 4, 4]:
        +---+---+---+---+
        | 2 | 2 | 4 | 4 |
        +---+---+---+---+
    after moving to left:
        +---+---+---+---+
        | 4 | 0 | 8 | 0 |
        +---+---+---+---+
    the final result line = [4, 8, 0, 0]
    '''
    for i in range(3):
        if line[i] == line[i + 1]:
            moveflag = True
            line[i] *= 2  # the number on left shoul times 2
            line[i + 1] = 0  # put 0 on the right


def _left_move_aline(line):
    '''move a row to left, if there is a movement, retur True, else False:
    e.g.: line = [2, 0, 2, 8]:
        +---+---+---+---+
        | 2 |   | 2 | 8 |      <----move to left
        +---+---+---+---+
    it include 3 steps:
        1. move all numbers to left and fill the empty cells:
            +---+---+---+---+
            | 2 | 2 | 8 |   |
            +---+---+---+---+
        2. check if there is a collison, which means if there are two adjacent identical numbers
           these two numbers need to combine, the result of combination should be put on the left
           and the right side could be a empty cell
            +---+---+---+---+
            | 4 |   | 8 |   |
            +---+---+---+---+
        3. repeat step 1, and move all the numbers to the left to fill blank cells:
            +---+---+---+---+
            | 4 | 8 |   |   |
            +---+---+---+---+
        final result: line = [4, 8, 0, 0]
    '''
    moveflag = False
    if _left_move_number(line):
        moveflag = True
    if _left_merge_number(line):
        moveflag = True
    if _left_move_number(line):
        moveflag = True
    return moveflag


def left():
    """when player press left button"""
    moveflag = False  # moveflag will be True if anything moved, else moveflag be False

    # move 1st row to left, if it could be moved or moved, return True
    for line in _map_data:
        if _left_move_aline(line):
            moveflag = True
    return moveflag


def right():
    """this is the algorithm when player press right button, or swipe right on a tablet
    we could reverse the whole screen, and after the reverse, right will be like left();
    after the operation, we reverse the screen back.
    """
    # switch around again
    for r in _map_data:
        r.reverse()
    moveflag = left()  # move to left
    # switch around again
    for r in _map_data:
        r.reverse()
    return moveflag


def up():
    """when player press up button, or swipe upward on screen
    1st append all the element in the same column in a line, and then operate
    after the operationg, we put the number back
    """
    moveflag = False
    for col in range(4):  # take the numbers in same column first
        # append every number in a line
        line = [0, 0, 0, 0]  # initial a line, so we could put numbers
        for row in range(4):
            line[row] = _map_data[row][col]
        # moving up in a column is moving to the left in line
        if (_left_move_aline(line)):
            moveflag = True
        # after the operation, put the numbers back to the vertical column
        for row in range(4):
            _map_data[row][col] = line[row]
    return moveflag


def down():
    """when player press down, or swipe down
    we switch the whole map upside down, and now down() is like up()
    after the operation, switch the map back
    """
    _map_data.reverse()
    moveflag = up()  # move upward
    _map_data.reverse()
    return moveflag


# -------------------------below are the game interface of 2048---------------------------
import sys

if (sys.version_info > (3, 0)):
    from tkinter import *
    from tkinter import messagebox
else:
    from Tkinter import *


def main():
    reset()  # we reset all the data

    root = Tk()  # creat a tkinter panel
    root.title('2048 - Yuanfeng Li Challenge!!!')  # set the title
    root.resizable(width=False, height=False)  # set the height and width 

    # below are the settings for keyboard
    keymap = {
        'a': left,
        'd': right,
        'w': up,
        's': down,
        'Left': left,
        'Right': right,
        'Up': up,
        'Down': down,
        'q': root.quit,
    }

    game_bg_color = "#bbada0"  # set the background of panel

    # set the color for each data in the game
    mapcolor = {
        0: ("#cdc1b4", "#776e65"),
        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#f9f6f2"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#e4c02a", "#f9f6f2"),
        1024: ("#e2ba13", "#f9f6f2"),
        2048: ("#ecc400", "#f9f6f2"),
        4096: ("#ae84a8", "#f9f6f2"),
        8192: ("#b06ca8", "#f9f6f2"),
        # ----others will use color 8192---------
        2**14: ("#b06ca8", "#f9f6f2"),
        2**15: ("#b06ca8", "#f9f6f2"),
        2**16: ("#b06ca8", "#f9f6f2"),
        2**17: ("#b06ca8", "#f9f6f2"),
        2**18: ("#b06ca8", "#f9f6f2"),
        2**19: ("#b06ca8", "#f9f6f2"),
        2**20: ("#b06ca8", "#f9f6f2"),
    }

    def on_key_down(event):
        'press buttons on keyboards and implement functions'
        keysym = event.keysym
        if keysym in keymap:
            if keymap[keysym]():  # if any number moved
                fill2()  # fill a new number, which is 2
        update_ui()
        if is_gameover():
            mb = messagebox.askyesno(
                title="gameover", message="Game is over!\nQuit or not?!")
            if mb:
                root.quit()
            else:
                reset()
                update_ui()

    def update_ui():
        '''update the user interface
        update all the settings and data based on the data we have
        '''
        for r in range(4):
            for c in range(len(_map_data[0])):
                number = _map_data[r][c]  # set numbers
                label = map_labels[r][c]  # choose Lable
                label['text'] = str(number) if number else ''
                label['bg'] = mapcolor[number][0]
                label['foreground'] = mapcolor[number][1]
        label_score['text'] = str(get_score())  # reset the score

    # create a new fram panel, it will have all the widget units
    frame = Frame(root, bg=game_bg_color)
    frame.grid(sticky=N+E+W+S)
    # set focus so it can receive the controls from buttons
    frame.focus_set()
    frame.bind("<Key>", on_key_down)

    # initialize the graphical interface 
    # create 4x4 
    map_labels = []  # the different labes, able Widget
    for r in range(4):
        row = []
        for c in range(len(_map_data[0])):
            value = _map_data[r][c]
            text = str(value) if value else ''
            label = Label(frame, text=text, width=4, height=2,
                          font=("Times", 30, "bold"))
            label.grid(row=r, column=c, padx=5, pady=5, sticky=N+E+W+S)
            row.append(label)
        map_labels.append(row)

    # set the score's lable
    label = Label(frame, text='Score', font=("Times", 30, "bold"),
                  bg="#bbada0", fg="#eee4da")
    label.grid(row=4, column=0, padx=5, pady=5)
    label_score = Label(frame, text='0', font=("Times", 30, "bold"),
                        bg="#bbada0", fg="#ffffff")
    label_score.grid(row=4, columnspan=2, column=1, padx=5, pady=5)

    # set the restart button
    def reset_game():
        reset()
        update_ui()

    restart_button = Button(frame, text='Restart', font=("Times", 16, "bold"),
                            bg="#8f7a66", fg="#f9f6f2", command=reset_game)
    restart_button.grid(row=4, column=3, padx=5, pady=5)

    update_ui()  # refresh interface

    root.mainloop()  # enter the main loop of tkinter


main()  # start game
