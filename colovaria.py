### co-loh-VA-ree-ah!

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



gol = tk.Canvas(width=400,height=400, highlightthickness=0, bg="black") #bd=-2

def colovaria():
    #x, y = 0, 0
    World = np.array([[0,0,1,1],[1,0,1,0],[0,0,1,1],[1,0,0,1]])
    #print(World)
    for cx in range(len(World)):
        for cy in range(len(World[cx])):
            #if World[0][cx] == 1:
            #print(int(x/12), int(y/12), cx, cy)
            print(cx+10,cy+10)
            if World[cx][cy] == 1:
                gol.create_rectangle(cx*10,cy*10,cx*10+10,cy*10+10, fill="white")
                # create_rectangle(x1,y1,x2,y2,clr) -> drawRect(pos[x,y],size[w,h],clr[r,g,b])
                print("\-> yes")
            else:
                print("\-> no")
            #y += 10 + 2
        #y = 0
        #x += 10 + 2


gol.pack()

#scrll = tk.Scrollbar(orient="horizontal", width=400)
#gol.xview_scroll(20,"units")
#scrll.pack()
#gol.xview_scroll(100, "units")



#main = tk.Frame(bg="#d1d2d1", width=win.winfo_width(), height=win.winfo_height()).pack()
#def info():
    #print(win.winfo_width(), win.winfo_height())

#hw = tk.Label(text="Hello, world!").pack()
#pressMe = ttk.Button(text="Press Me!", command=info).pack()

colovaria()

win.mainloop()
