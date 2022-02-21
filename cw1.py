from tkinter import *
import random

def left_click(index):
    global mine_field, map, display_bar, stack, close, row, col, mines, gameover, flag_map, flags, lab_flag
    if index in close or gameover or index in flag_map:
        return
    if map[index] == "b":
        lab_over = Label(display_bar, text = "Game is Over!!")
        lab_over.pack()
        game_over()
        return
    stack.append(index)
    while len(stack) > 0:
        cl_ind = stack[-1]
        cl_exam = examine(cl_ind)
        close.append(cl_ind)
        stack.pop()
        if cl_exam == 0:
            for i in surrounding(cl_ind):
                if i not in close and i not in stack:
                    stack.append(i)
            mine_field[cl_ind].config(bg = "#002633")
            # mine_field[cl_ind].config(bg = "#002633")
        else:
            mine_field[cl_ind].config(text = str(cl_exam))
    for i in flag_map:
        if i in close:
            mine_field[i].config(text="   ", fg="0099cc")
            flags += 1
            flag_map.remove(i)
    lab_flag.config(text="Mines: " + str(flags))
    if len(close) == row*col-mines:
        lab_over = Label(display_bar, text="You have Won!")
        lab_over.pack()
        game_over()


def surrounding(index):
    global row, col
    test = []
    for c in [-col,0,col]:
        if index + c <0 or index+c >= row*col:
            continue
        for i in [-1,0,1]:
            if index//col != (index+i)//col:
                continue
            test.append(index+c+i)
    test.remove(index)
    return test


def examine(index):
    total = 0
    for i in surrounding(index):
        if map[i]=="b":
            total+=1
    return total



def first_left_click(index):
    global map, row, col, mines, mine_field, lab_flag, flags
    map = ["b" for i in range(mines)] + ["" for i in range(row * col - mines)]
    random.shuffle(map)
    while map[index] == "b":
        random.shuffle(map)
    for i in range(row * col):
        mine_field[i].config(command=lambda x=i: left_click(x))
        mine_field[i].bind('<Button-3>', lambda eff, x=i: right_click(event=eff, index=x))
    lab_flag.config(text="Mines: "+str(flags))
    left_click(index)


def game_over():
    global gameover
    gameover = True
    for i in range(row*col):
        if map[i] == "b":
            mine_field[i].config(text="💣", fg= "black")


def right_click(event, index):
    global flag_map, close, mine_field, flags, lab_flag
    if index in close or gameover:
        return
    if index in flag_map:
        mine_field[index].config(text="   ", fg = "black")
        flags += 1
        flag_map.remove(index)
    elif flags>0:
        mine_field[index].config(text=" ! ", fg="green")
        flags -= 1
        flag_map.append(index)
    lab_flag.config(text="Mines: "+str(flags))

def reset():
    pass

gameover = False
row = 15
col = 20
mines = 40
flags = mines

minesweeper = Tk()
minesweeper.title('Mine Sweeper')

fr_tbar = LabelFrame(minesweeper)
fr_tbar.grid(row=0, column=0)

fr_game = LabelFrame(minesweeper)
fr_game.grid(row=1, column=0)

display_bar = LabelFrame(minesweeper)
display_bar.grid(row=2, column=0)

lab_flag = Label(fr_tbar, text = "Mines: --")
lab_flag.grid(row=0, column=0)

btn_reset = Button(minesweeper,text="Reset")
btn_reset.grid(row=10, column=0)

stack = []
close = []
flag_map = []

mine_field = []
for i in range(row*col): # i=0,1,2,,,,row*col-1
    mine_field.append(Button(fr_game, text= "   ", command= lambda x=i: first_left_click(x)))  # mine_field = [Button(fr_game, text, command=first_click(0), Button(fr_game, text, command=first_click(1), Button(fr_game, text, command=first_click(2), ... Button(fr_game, text, command=first_click(row*col-1)]
    mine_field[i].grid(row=i//col, column= i%col) # finally button position is defined by using grid
    # when u actually press button i, then command=first_click(i) happens

minesweeper.mainloop()  # game loop continuation!!