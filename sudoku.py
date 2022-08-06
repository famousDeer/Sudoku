import pygame as pg
from pygame.locals import *
import copy
import time
import random
import pulp as plp

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
    solve(board_num)
    if len(solve_board) == 1:
        board_num = copy.deepcopy(create_board(level))
    return board_num

# Function drawing board with numbers
def draw_board(mouse_pos, play_time, mouse_pos_click):
    global lost, start, board_num, reset_board, lose_strike, level, solve_board
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
                solve_board = [[]]
                while len(solve_board) == 1:
                    board_num = create_board(level)
                    solve(board_num)
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

# New Solver works better
def default_sudoku_constraints(prob, grid_vars, rows, cols, grids, values):
    # Constraint to ensure only one value is filled for a cell
    for row in rows:
        for col in cols:
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value] for value in values]),
                                        sense=plp.LpConstraintEQ, rhs=1, name=f"constraint_sum_{row}_{col}"))


    # Constraint to ensure that values from 1 to 9 is filled only once in a row        
    for row in rows:
        for value in values:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for col in cols]),
                                        sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_row_{row}_{value}"))

    # Constraint to ensure that values from 1 to 9 is filled only once in a column        
    for col in cols:
        for value in values:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for row in rows]),
                                        sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_col_{col}_{value}"))


    # Constraint to ensure that values from 1 to 9 is filled only once in the 3x3 grid       
    for grid in grids:
        grid_row  = int(grid/3)
        grid_col  = int(grid%3)

        for value in values:
            prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[grid_row*3+row][grid_col*3+col][value]*value  for col in range(0,3) for row in range(0,3)]),
                                        sense=plp.LpConstraintEQ, rhs=value, name=f"constraint_uniq_grid_{grid}_{value}"))

def prefilled_constraints(prob, input_sudoku, grid_vars, rows, cols, values):
    for row in rows:
        for col in cols:
            if(input_sudoku[row][col] != 0):
                prob.addConstraint(plp.LpConstraint(e=plp.lpSum([grid_vars[row][col][value]*value  for value in values]), 
                                                    sense=plp.LpConstraintEQ, 
                                                    rhs=input_sudoku[row][col],
                                                    name=f"constraint_prefilled_{row}_{col}"))

def extract_solution(grid_vars, rows, cols, values):
    solution = [[0 for col in cols] for row in rows]
    grid_list = []
    for row in rows:
        for col in cols:
            for value in values:
                if plp.value(grid_vars[row][col][value]):
                    solution[row][col] = value 
    return solution

def solve(input_sudoku):
    global solve_board
    prob = plp.LpProblem("Sudoku Solver")
    rows = range(0,9)
    cols = range(0,9)
    grids = range(0,9)
    values = range(1,10)

    grid_vars = plp.LpVariable.dicts("grid_value", (rows, cols, values), cat='Binary')

    objective = plp.lpSum(0)
    prob.setObjective(objective)

    default_sudoku_constraints(prob, grid_vars, rows, cols, grids, values)

    prefilled_constraints(prob, input_sudoku, grid_vars, rows, cols, values)

    prob.solve()
    solution_status = plp.LpStatus[prob.status]
    print(f'Solution Status = {plp.LpStatus[prob.status]}')
    if solution_status == 'Optimal':
        solve_board = copy.deepcopy(extract_solution(grid_vars, rows, cols, values))

# Old solver works fine but sometimes can hit max recursion depth
# Function solving entire board 
# def solve():
#     global board_num, solve_board
#     for y in range(9):
#         for x in range(9):
#             if board_num[y][x] == 0:
#                 for n in range(1, 10):
#                     if possible(y, x, n):
#                         board_num[y][x] = n
#                         solve()
#                         board_num[y][x] = 0
#                 return
#     solve_board = copy.deepcopy(board_num)

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

# Function creating menu buttons
def menu_buttons(btn_rec, btn_label, label_pos, mouse_pos):
    if btn_rec.collidepoint(mouse_pos):
        pg.draw.rect(screen, colour_highlight, btn_rec)
    pg.draw.rect(screen, Black, btn_rec, 2)
    screen.blit(font_button.render(btn_label, True, Black), label_pos)
    
# Function creating menu
def menu():
    global level, board_num, reset_board, loop
    mouse_pos = pg.mouse.get_pos()
    easy_btn = pg.Rect(375, 450, 200, 50)
    medium_btn = pg.Rect(375, 525, 200, 50)
    hard_btn = pg.Rect(375, 600, 200, 50)
    menu_buttons(easy_btn, "Easy", (435, 455), mouse_pos)
    menu_buttons(medium_btn, "Medium", (415, 530), mouse_pos)
    menu_buttons(hard_btn, "Hard", (435, 605), mouse_pos)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            loop = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if easy_btn.collidepoint(mouse_pos):
                level = 30
            elif medium_btn.collidepoint(mouse_pos):
                level = 28
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
                solve_board = [[]]
            pos_write_num = pg.mouse.get_pos()
        elif event.type == pg.KEYUP:
            user_input(pos_write_num)
    clock.tick(120) # 120 FPS
    pg.display.flip()
