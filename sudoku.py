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
reset_board = copy.deepcopy(board_num)
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
new_game_btn = pg.Rect(400, 1000, 20, 20)
new_game_btn_col = White

#TIME
start = time.time()

#Default mouse position
pos_write_num = (0, 0)
mouse_pos_click = (0, 0)

#DIFFICULTY
level = 0

# Function creating board depending on chosen lvl
def create_board(level):
    global board_num, reset_board, solve_board
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
    while num < level:
        pos_x = random.randrange(0, 9)
        pos_y = random.randrange(0, 9)
        numb = random.randrange(1, 10)
        if possible(pos_y, pos_x, numb) and board_num[pos_y][pos_x] == 0:
            num += 1
            board_num[pos_y][pos_x] = numb
    solve()
    if len(solve_board) == 1:
        board_num = copy.deepcopy(create_board(level))
    return board_num

# Function drawing board with numbers
def draw_board(mouse_pos, play_time, mouse_pos_click):
    global lost, start, board_num, reset_board, lose_strike, level
    # Rectangle parameters
    width = 100
    height = 100
    pos_x = 25
    pos_y = 50

    # Highlight rectangle parameters
    pos_x_highlight = ((mouse_pos[0] - 25) // 100) * 100 + 25
    pos_y_highlight = ((mouse_pos[1] - 50) // 100) * 100 + 50

    # Rectangle on click position
    pos_x_mouse = ((mouse_pos_click[0] - 25) // 100) * 100 + 25
    pos_y_mouse = ((mouse_pos_click[1] - 50) // 100) * 100 + 50
    #Screen refreshing only if player didn't lose
    if not lost:
        screen.fill(Background)
        if level > 0:
            buttons(reset_btn_col, reset_btn, "Reset", (80, 990))
            buttons(highlight_btn_col, highlight_btn, "Highlight", (230, 990))
            buttons(new_game_btn_col, new_game_btn, "New Game", (430, 990))
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
            if pos_x_mouse >= 25 and pos_x_mouse < 925 and pos_y_mouse >= 50 and pos_y_mouse < 950:
                pg.draw.rect(screen, Red, (pos_x_mouse, pos_y_mouse, width, height), 5)
        else:
            level = copy.deepcopy(menu())
            start = time.time()
    # If it's lost board will freeze and labels will show up
    else:
        screen.blit(font.render("Game over", True, Red), (250, 400))
        if screen.blit(font_button.render("Play again", True, Red), (400, 500)).collidepoint(pg.mouse.get_pos()):
            screen.blit(font_button.render("Play again", True, Gray), (400, 500))
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                start = time.time()
                board_num = create_board(level)
                while len(solve_board) == 1:
                    board_num = create_board(level)
                    solve()
                reset_board = copy.deepcopy(board_num)
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

# Function creating menu
def menu():
    global level, board_num, reset_board, loop
    easy_btn = pg.Rect(375, 450, 200, 50)
    medium_btn = pg.Rect(375, 525, 200, 50)
    hard_btn = pg.Rect(375, 600, 200, 50)
    mouse_pos = pg.mouse.get_pos()
    if easy_btn.collidepoint(mouse_pos):
        pg.draw.rect(screen, colour_highlight, easy_btn)
    elif medium_btn.collidepoint(mouse_pos):
        pg.draw.rect(screen, colour_highlight, medium_btn)
    elif hard_btn.collidepoint(mouse_pos):
        pg.draw.rect(screen, colour_highlight, hard_btn)
    pg.draw.rect(screen, Black, easy_btn, 2)
    pg.draw.rect(screen, Black, medium_btn, 2)
    pg.draw.rect(screen, Black, hard_btn, 2)
    screen.blit(font_button.render("Easy", True, Black), (435, 455))
    screen.blit(font_button.render("Medium", True, Black), (415, 530))
    screen.blit(font_button.render("Hard", True, Black), (435, 605))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            loop = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if easy_btn.collidepoint(mouse_pos):
                level = 32
            elif medium_btn.collidepoint(mouse_pos):
                level = 30
            elif hard_btn.collidepoint(mouse_pos):
                level = 26           
    if level > 0:
        board_num = create_board(level)
        reset_board = copy.deepcopy(board_num)
    return level

loop = True

while loop:
    play_time = round(time.time() - start) # Calculating play time in sec 
    draw_board(pg.mouse.get_pos(), play_time, mouse_pos_click)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            loop = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            # Mouse click position
            mouse_pos_click = pg.mouse.get_pos()
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
            # Hit new game button
            elif new_game_btn.collidepoint(pg.mouse.get_pos()):
                level = 0
            pos_write_num = pg.mouse.get_pos()
        elif event.type == pg.KEYUP:
            user_input(pos_write_num)
    clock.tick(120) # 120 FPS
    pg.display.flip()
