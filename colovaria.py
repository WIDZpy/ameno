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
CamY = 0
CamSpeed = 4

gol = tk.Canvas(win, width=400,height=400, highlightthickness=0, bg="black") #bd=-2

def colovaria():
    #x, y = 0, 0
    #World = np.array([[0,0,1,1],[1,0,1,0],[0,0,1,1],[1,0,0,1]])
    #print(World)
    World = lumos.lumos(8,8)
    for cx in range(len(World)):
        # watch out for this: 'cx in World' gives cx the value of the currently targeted element, whereas 'cx in range(len(World))' gives cx the value of the index of the currently targeted element, so that it acts as "it should", or rather as "I expect it to". This way cx refers to the number of iterations, and World[cx] returns the value corresponding to this index. (also 'len()' is used, I get why but I'll do some testing to see what happens without it, someday I'll do it, I swear)                   *no*
        for cy in range(len(World[cx])):
            #if World[0][cx] == 1:
            #print(int(x/12), int(y/12), cx, cy)
            #print(cx+10,cy+10)
            if World[cx][cy] == 1:
                gol.create_rectangle(cx*10,cy*10,cx*10+10,cy*10+10, fill="white")
                #print("\-> yes")
            #else:
                #print("\-> no")
            #y += 10 + 2
        #y = 0
        #x += 10 + 2


gol.pack()


tools = ttk.Frame(win, padding=4)

move = tk.Frame(tools)
#tools = tk.Frame(win, pady=4, bg="")
btn_left = ttk.Button(move, text="<-", width=8).pack(side="left")
btn_up = ttk.Button(move, text="^^", width=8).pack(side="left")
btn_down = ttk.Button(move, text="vv", width=8, command="print(CamX)").pack(side="left")
btn_right = ttk.Button(move, text="->", width=8, command="CamX+=CamSpeed").pack(side="left")
move.pack(side="left")

zoom = tk.Frame(tools)
btn_in = ttk.Button(move, text="+", width=8).pack(side="left")
btn_out = ttk.Button(move, text="-", width=8).pack(side="left")
zoom.pack(side="right")

tools.pack()



colovaria()

win.mainloop()
