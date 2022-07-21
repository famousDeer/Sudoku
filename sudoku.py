import pygame as pg
from pygame.locals import *
import copy
import time
import random

#END GAME
lost = False
lose_strike = 0

#COLORS
Background = (200, 200, 200)
Black = (0, 0, 0)
Gray = (100, 100, 100)
Green = (0, 255, 0)
Red = (255, 0, 0)
White = (255, 255, 255)

#HIGHLIGHT RECTANGLE
colour_highlight = (125, 187, 212) #Light Blue
highlight_on = True

#BOARD
board_num = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
solve_board = [[]]

#FPS
clock = pg.time.Clock()

#DISPLAY
pg.init()
screen = pg.display.set_mode((950, 1100))

#TEXT
font = pg.font.SysFont('arial', 90)
font_button = pg.font.SysFont('arial', 35)

#BUTTONS
reset_btn = pg.Rect(50, 1000, 20, 20)
reset_btn_col = Black
highlight_btn = pg.Rect(200, 1000, 20, 20)
highlight_btn_col = Green

#TIME
start = time.time()

#Default mouse position
pos_write_num = (0, 0)

# Function creating board depending on chosen lvl
def create_board():
    global board_num
    board_num = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    num = 0
    while num < 30:
        pos_x = random.randrange(0, 8)
        pos_y = random.randrange(0, 8)
        numb = random.randrange(1, 10)
        if possible(pos_y, pos_x, numb) and board_num[pos_y][pos_x] == 0:
            num += 1
            board_num[pos_y][pos_x] = numb
    return board_num

# Function drawing board with numbers
def draw_board(mouse_pos, play_time):
    global lost, start, board_num, reset_board, lose_strike
    # Rectangle parameters
    width = 100
    height = 100
    pos_x = 25
    pos_y = 50

    # Highlight rectangle parameters
    pos_x_highlight = ((mouse_pos[0] - 25) // 100) * 100 + 25
    pos_y_highlight = ((mouse_pos[1] - 50) // 100) * 100 + 50
    #Screen refreshing only if player didn't lose
    if not lost:
        screen.fill(Background)
        screen.blit(font_button.render(time_format(play_time), True, Black), (400, 10))
        if highlight_on:
            if pos_x_highlight >= 25 and pos_x_highlight < 925 and pos_y_highlight >= 50 and pos_y_highlight < 950:
                pg.draw.rect(screen, colour_highlight, (pos_x_highlight, 50, width, 900))
                pg.draw.rect(screen, colour_highlight, (25, pos_y_highlight, 900, height))
        # Drawing a board using line 
        for i in range(0, 10):
            for j in range(0, 10):
                if j < 9 and i < 9 and board_num[j][i] != 0:
                    # Numbers, that is untouchable will be black, wrong numbers will be red, user input number will be gray
                    if board_num[j][i] == reset_board[j][i]:
                        screen.blit(font.render(str(board_num[j][i]), True, Black), (pos_x + 25 + (i * 100), pos_y + (j * 100)))
                    elif len(solve_board) > 1 and board_num[j][i] != solve_board[j][i]:
                        screen.blit(font.render(str(board_num[j][i]), True, Red), (pos_x + 25 + (i * 100), pos_y + (j * 100)))
                    else:
                        screen.blit(font.render(str(board_num[j][i]), True, Gray), (pos_x + 25 + (i * 100), pos_y + (j * 100)))
                # Drawing board
                if j % 3 == 0 and i == 0:
                    pg.draw.line(screen, Black, (25 + j * 100, 50), (25 + j * 100, 950), 5)
                    pg.draw.line(screen, Black, (23, 50 + j * 100), (927, 50 + j * 100), 5)
                elif i == 0:
                    pg.draw.line(screen, Black, (25 + j * 100, 50), (25 + j * 100, 950), 2)
                    pg.draw.line(screen, Black, (23, 50 + j * 100), (927, 50 + j * 100), 2)
    # If it's lost board will freeze and labels will show up
    else:
        screen.blit(font.render("Game over", True, Red), (250, 400))
        if screen.blit(font_button.render("Play again", True, Red), (400, 500)).collidepoint(pg.mouse.get_pos()):
            screen.blit(font_button.render("Play again", True, Gray), (400, 500))
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                start = time.time()
                board_num = copy.deepcopy(reset_board)
                lost = False
                lose_strike = 0
        else:
            screen.blit(font_button.render("Play again", True, Red), (400, 500))
            
# Function checks if it possible to write number in specific position
def possible(y, x, n):
    global board_num
    for i in range(0, 9):
        if board_num[y][i] == n:
            return False
    for i in range(0, 9):
        if board_num[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if board_num[y0+i][x0+j] == n:
                return False
    return True

# Function solving entire board 
def solve():
    global board_num, solve_board
    for y in range(9):
        for x in range(9):
            if board_num[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        board_num[y][x] = n
                        solve()
                        board_num[y][x] = 0
                return
    solve_board = copy.deepcopy(board_num)

# Function writing number on specific position from user and counting wrong numbers
def user_input(position_num):
    global lose_strike, lost
    pos_x = ((position_num[0] - 25) // 100)
    pos_y = ((position_num[1] - 50) // 100)
    if pos_x >= 0 and pos_x < 9 and pos_y >= 0 and pos_y < 9:
        if (event.key == pg.K_1 or event.key == pg.K_KP1) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 1
        elif (event.key == pg.K_2 or event.key == pg.K_KP2) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 2
        elif (event.key == pg.K_3 or event.key == pg.K_KP3) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 3
        elif (event.key == pg.K_4 or event.key == pg.K_KP4) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 4
        elif (event.key == pg.K_5 or event.key == pg.K_KP5) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 5
        elif (event.key == pg.K_6 or event.key == pg.K_KP6) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 6
        elif (event.key == pg.K_7 or event.key == pg.K_KP7) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 7
        elif (event.key == pg.K_8 or event.key == pg.K_KP8) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 8
        elif (event.key == pg.K_9 or event.key == pg.K_KP9) and reset_board[pos_y][pos_x] == 0:
            board_num[pos_y][pos_x] = 9
        
        if board_num[pos_y][pos_x] != solve_board[pos_y][pos_x]:
            lose_strike += 1
        if lose_strike == 4:
            lost = True

# Function converting time to min and sec
def time_format(times):
    sec = times % 60
    minute = times // 60
    format = str(minute) + " min " + str(sec) + " sec"
    return format

# Function creating buttons
def buttons(btn_color, btn_rec, btn_label, btn_pos):
    pg.draw.rect(screen, btn_color, btn_rec)
    screen.blit(font_button.render(btn_label, True, Black), btn_pos)

loop = True
# While loop will work that long as created random board is solvable
board_num = copy.deepcopy(create_board())
solve()
while len(solve_board) == 1:
    board_num = copy.deepcopy(create_board())
    solve()
reset_board = copy.deepcopy(board_num)

while loop:
    play_time = round(time.time() - start) # Calculating play time in sec 
    draw_board(pg.mouse.get_pos(), play_time)
    buttons(reset_btn_col, reset_btn, "Reset", (80, 990))
    buttons(highlight_btn_col, highlight_btn, "Highlight", (230, 990))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            loop = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            # Hit reset buttun
            if reset_btn.collidepoint(pg.mouse.get_pos()):
                board_num = copy.deepcopy(reset_board)
                start = time.time()
                lose_strike = 0
            # Hit highlight button
            elif highlight_btn.collidepoint(pg.mouse.get_pos()):
                highlight_on = not highlight_on
                if highlight_on:
                    highlight_btn_col = Green
                else:
                    highlight_btn_col = Gray
            pos_write_num = pg.mouse.get_pos()
        elif event.type == pg.KEYUP:
            user_input(pos_write_num)
    clock.tick(120) # 120 FPS
    pg.display.flip()
