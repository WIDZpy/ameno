### co-loh-VA-ree-ah!
#import maraudeurs
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np

class Window:

    def __init__(self):
        '''frame=div, label=text, entry=field
        use .pack() at the end of the line rather than adding a new line and referencing your object for no reason, it's ugly and it takes space, just like this looooong comment
        the line above is not always true actually'''

        #self.life = maraudeurs.Life()
        self.win = tk.Tk()
        self.win.geometry("800x600")
        self.win.title("Welland's Game of Life")
        self.win.configure(bg="#d1d2d1", padx=25, pady=25)
        self.gol = tk.Canvas(width=400,height=400, highlightthickness=0, bg="black") #bd=-2
        self.World = np.array([[0,0,1,1,1],[1,0,1,0,1],[0,0,1,1,1],[1,0,0,1,1],[1,1,1,1,1]])


    def colovaria(self):

        for cx in range(len(self.World)):

            for cy in range(len(self.World[cx])):

                if self.World[cx][cy] == 1:

                    self.gol.create_rectangle(cx*10,cy*10,cx*10+10,cy*10+10, fill="white")

        self.gol.pack()





truv = Window()
truv.colovaria()
truv.win.mainloop()
