### co-loh-VA-ree-ah!

import lumos
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
# frame=div, label=text, entry=field
# use .pack() at the end of the line rather than adding a new line and referencing your object for no reason, it's ugly and it takes space, just like this looooong comment
# the line above is not always true actually

win = tk.Tk()
win.geometry("800x600")
win.title("Welland's Game of Life")
win.configure(bg="#d1d2d1", padx=25, pady=25)

CamX = 0
'''Camera X position'''
CamY = 0
'''Camera Y position'''
CamW = 40
'''Camera Width, or X size'''
CamH = 40
'''Camera Height, or Y size'''

CellSize = 10
'''The size of each cell. May be modified at moment, it will be taken into account the next frame.'''

World = lumos.lumos(8,8,4)


gol = tk.Canvas(win, width=400,height=400, highlightthickness=0, bg="black") #bd=-2
gol.pack()

def colovaria():
    global World
    #World = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
    View = World[int(CamX/CellSize):int(CamX/CellSize)+int(CamW/CellSize), int(CamY/CellSize):int(CamY/CellSize)+int(CamH/CellSize)]
    print(View, "\n")
    for cx in range(len(View)):
        # watch out for this: 'cx in World' gives cx the value of the currently targeted element, whereas 'cx in range(len(World))' gives cx the value of the index of the currently targeted element, so that it acts as "it should", or rather as "I expect it to". This way cx refers to the number of iterations, and World[cx] returns the value corresponding to this index. (also 'len()' is used, I get why but I'll do some testing to see what happens without it, someday I'll do it, I swear)                   *no*
        for cy in range(len(View[cx])):
            if View[cx][cy] == 1:
                gol.create_rectangle(cx*CellSize,cy*CellSize,cx*CellSize+10,cy*CellSize+10, fill="white")




def left():
    global CamX
    CamX -= 5
def up():
    global CamY
    CamY += 5
def down():
    global CamY
    CamY -= 5
def right():
    global CamX
    CamX += 5
def zoomIn():
    print(CamX,CamY,"\n")
def zoomOut():
    colovaria()
    gol.update()


def init():
    tools = ttk.Frame(win, padding=4)

    move = tk.Frame(tools)
    #tools = tk.Frame(win, pady=4, bg="")
    btn_left = ttk.Button(move, text="<-", width=8, command=left).pack(side="left")
    btn_up = ttk.Button(move, text="^^", width=8, command=up).pack(side="left")
    btn_down = ttk.Button(move, text="vv", width=8, command=down).pack(side="left")
    btn_right = ttk.Button(move, text="->", width=8, command=right).pack(side="left")
    move.pack(side="left")

    zoom = tk.Frame(tools)
    btn_in = ttk.Button(move, text="+", width=8, command=zoomIn).pack(side="left")
    btn_out = ttk.Button(move, text="-", width=8, command=zoomOut).pack(side="left")
    zoom.pack(side="right")

    tools.pack()


while True:
    init()
    colovaria()
    win.mainloop()

