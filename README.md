# :round_pushpin: General info
Hello, this is my first project by my self in python. It's very basic idea of sudoku created using pygame. It include highlighting row and column with a current position of your mouse (you can turn that off). It has also solver to create random new board.
# :open_file_folder: Table of Contents
* [Presentation](#fire-presentation)
* [Menu](#pagefacingup-menu)
* [Highlight](#gem-highlight)
* [Lost the game](#x-lost-the-game)
* [Reset Board](#arrowscounterclockwise-reset-board)
* [New Game](#back-new-game)
* [Solver](#ghost-solver)
* [Future functions](#bulb-future-functions)
* [Known Issues](#ladybeetle-known-issues)

# :fire: Presentation

## :page_facing_up: Menu
You have 3 levels to choose. Levels depends on how many numbers you will see on the board.

<div id="header" align="center">
    <img src=./Photos/Menu.gif>
</div>

## :gem: Highlight
Wherever your cursor is pointing, row and column will be highlighted. You can also disable this future, by clicking in green rectangle.

<div id="header" align="center">
    <img src=./Photos/Board_with_highlight.gif>
</div>

## :x: Lost the game
After 3 missed numbers, the next one will result in a loss.

<div id="header" align="center">
    <img src=./Photos/Game_Over.gif>
</div>

## :arrows_counterclockwise: Reset board
If you don't put up with mistakes, there is tiny black rectangle with label "Reset". One click and boom, no one saw your mistake.

<div id="header" align="center">
    <img src=./Photos/Reset.gif>
</div>

## :back: New Game
If you wanna start new game, just click white button and choose level again

<div id="header" align="center">
    <img src=./Photos/New_Game.gif>
</div>

## :ghost: Solver
I used solver from this site :point_right: https://towardsdatascience.com/solve-sudoku-using-linear-programming-python-pulp-b41b29f479f3 

# :bulb: Future Functions
* :heavy_check_mark: Game over create new board
* :heavy_check_mark: Menu
* :heavy_check_mark: Difficult levels
* :heavy_check_mark: New Game button
* :lock: Highlight other numbers on click
* :lock: Complete level window
# :lady_beetle: Known Issues
* :heavy_check_mark: ~~New Game button do not create new board~~
* :x: Creating new board on easy level can take some time
* :x: Any button can count as a wrong number

