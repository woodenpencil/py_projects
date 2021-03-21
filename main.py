import tkinter as tk
from tkinter import Tk, Canvas
from random import shuffle
from tkinter import *

b_size = 4
s_size = 80
empty_s = b_size ** 2
root = Tk()
root.title("Fifteen game")

root.label = tk.Label(root, text="")
root.label.pack()
root.remaining = 0
root.timeup = False

root.count_cl = tk.Label(root, text="")
root.count_cl.pack()

def init_game():
    root.clicks = 0
    show_clicks()
    root.remaining=0
    root.timeup = False
    shuffle(board)
    while not is_solvable():
        shuffle(board)
    root.remaining = 180
    draw_board()

nw_game = tk.Button(root, text="New game", fg="green", command=init_game)
nw_game.pack(fill=X)

def countdown(remaining=None):
    """creates timetable with time during which you can solve the game"""
    if remaining is not None:
        root.remaining = remaining
    if root.remaining <= 0:
        root.timeup = True
        root.label.configure(text="Time is up!")
        return
    else:
        root.label.configure(text="Time left: %d" % root.remaining)
        root.remaining = root.remaining - 1
        root.after(1000, countdown)

def draw_board():
    """initializing board with rectangles"""
    c.delete('all')
    for i in range(b_size):
        for j in range(b_size):
            index = str(board[b_size * i + j])
            if index != str(empty_s):
                c.create_rectangle(j * s_size, i * s_size,
                                   j * s_size + s_size,
                                   i * s_size + s_size,
                                   fill='#19CCC0',
                                   outline='#FFFFFF')
                c.create_text(j * s_size + s_size / 2,
                              i * s_size + s_size / 2,
                              text=index,
                              font="Arial {} bold".format(int(s_size / 4)),
                              fill='#FFFFFF')

def show_clicks():
    root.count_cl.configure(text="Clicks: %d" % root.clicks)

def click(event):
    """handling click event"""
    x, y = event.x, event.y
    x = x // s_size
    y = y // s_size
    board_index = x + (y * b_size)
    empty_index = get_empty_neighbor(board_index)
    board[board_index], board[empty_index] = board[empty_index], board[board_index]
    root.clicks += 1
    show_clicks()
    draw_board()
    if board == correct_board:
        show_victory_plate()

def get_empty_neighbor(index):
    """search for neighbor empty rectangle"""
    empty_index = board.index(empty_s)
    abs_value = abs(empty_index - index)
    if abs_value == b_size:
        return empty_index
    elif abs_value == 1:
        max_index = max(index, empty_index)
        if max_index % b_size != 0:
            return empty_index
    return index

def show_victory_plate():
    """shows table after winning the game"""
    if root.timeup:
        return
    c.create_rectangle(s_size / 5,
                       s_size * b_size / 2 - 10 * b_size,
                       b_size * s_size - s_size / 5,
                       s_size * b_size / 2 + 10 * b_size,
                       fill='#000000',
                       outline='#FFFFFF')
    c.create_text(s_size * b_size / 2,
                  s_size * b_size / 1.9,
                  text="WIN!",
                  font="Arial {} bold".format(int(10 * b_size)),
                  fill='#00FF00')


def get_inv_count():
    """calculates inversions"""
    inversions = 0
    inversion_board = board[:]
    inversion_board.remove(empty_s)
    for i in range(len(inversion_board)):
        first_item = inversion_board[i]
        for j in range(i + 1, len(inversion_board)):
            second_item = inversion_board[j]
            if first_item > second_item:
                inversions += 1
    return inversions


def is_solvable():
    """decides weather game is possible to win or no"""
    num_inversions = get_inv_count()
    if b_size % 2 != 0:
        return num_inversions % 2 == 0
    else:
        empty_square_row = b_size - (board.index(empty_s) // b_size)
        if empty_square_row % 2 == 0:
            return num_inversions % 2 != 0
        else:
            return num_inversions % 2 == 0




c = Canvas(root, width=b_size * s_size, height=b_size * s_size, bg='#808080')
c.bind('<Button-1>', click)
c.pack()
board = list(range(1, empty_s + 1))
correct_board = board[:]
init_game()
countdown()
root.mainloop()