from math import *
import numpy as np
import pygame.image
import maraudersMap as backend
import pygame as pg
import mandragore

'''réorganisation'''

class Win:
    def __init__(self):
        self.window_caracteristique = {
            'title': "John Conway's Game of Life",
            'defintion': 64,
            'length side': 500,
            'border':4,

        }
        self.win = pg.display.set_mode((700, 700))
        self.CamX = 0
        self.CamY = 0
        self.winPrevMousePos = pg.mouse.get_pos()
        self.CellClr = (255, 255, 255)
        self.BgClr = (0, 0, 0)
        self.CamW = 64
        self.CamH = 64
        pg.display.set_icon(pygame.image.load('textures/logo.png'))
        pg.display.set_caption(self.window_caracteristique['title'])
        return

    def show(self):
        self.win = pg.display.set_mode((self.window_caracteristique['length side'] + self.window_caracteristique['border'] * 2,
                                        self.window_caracteristique['length side'] + self.window_caracteristique['border'] * 2))
        return

    def log(self):
        print()

    def aparecium(self, world):
        '''
        afiche un array dans la fenaitre pygame
        :param world: l'array a aficher dans la fenetre pygame
        '''
        global CamX, CamY
        CamX = mandragore.clamp(CamX, 0, world.shape[0] - CamW)
        CamY = mandragore.clamp(CamY, 0, world.shape[1] - CamH)
        # print(CamX,CamY)
        View = np.array(world[floor(CamY):floor(CamY) + CamH, floor(CamX):floor(CamX) + CamW])
        self.win.fill(BgClr)
        view_cordantate = np.array(np.where(View == 1)).tolist()
        for cy, cx in zip(view_cordantate[0], view_cordantate[1]):
            pg.draw.rect(self.win, self.CellClr, (cx * self.CellWH + self.GoLPosX, cy * self.CellWH + self.GoLPosY, CellWH, CellWH))





#'''le boirdel de maxime'''
#
#frameCount = 0
#
##win = pg.display.set_mode((1280,720))
#
#GoLPosX = 4
#GoLPosY = 4
#
#win = pg.display.set_mode((512+GoLPosX*2, 512+GoLPosY*2))
#pg.display.set_icon(pygame.image.load('textures/logo.png'))
#pg.display.set_caption("John Conway's Game of Life")
#
#
#
#winPrevMousePos = pg.mouse.get_pos()
#winMenuState = False
#winMenuPos = (0, 0)
#
#CamX = 0
#CamY = 0
#CamW = 64
#CamH = 64
#
#CellWH = 8
#CellClr = CellClrDef = (255, 255, 255)
#BgClr = BgClrDef = (0, 0, 0)
#
#
#
##World = lumos.lumos(4,4,3)
##World = np.array([[0,1,0,1],[0,1,1,0],[0,1,0,0],[1,0,0,1]])
#
##View = np.array(World)
##print(View)
#
##print()
#
##View = np.array(World[1:3,1:3])
##View.resize()
##print(View)
#
#
#
#StartWorld = np.zeros((128,128))
#life = backend.Life((128, 128))
## life.draw_adapt('canadagoose', (0,0), rotation=2)
#life.draw_adapt('scotsp5', (12, 22), rotation=2)
## life.global_current_life[10,11] = 1
## life.global_current_life[10,12] = 1
## life.global_current_life[10,10] = 1
## life.draw_random(size="fill")
#World = life.getlife()
#
#life.point_and_clic((0, 0))
#life.point_and_clic((1, 0))
#life.point_and_clic((2, 0))
#
#
#
#
#
#
#
#
#
#
#    #Empty[CamX:CamX+CamW,CamY:CamY+CamH] = View
#    #View.resize(4,4)
#    #print(CamX,CamY,"\n",View,"\n")
#    #for cx in range(len(View)):
#    #    for cy in range(len(View[cx])):
#    #
#    #        if View[cy, cx] == 1:
#    #            pg.draw.rect(win, CellClr, (cx*CellWH + GoLPosX, cy*CellWH + GoLPosY, CellWH, CellWH))
#            #else:
#                #pg.draw.rect(win, BgClr, (cx*CellWH, cy*CellWH, CellWH, CellWH))
#
#def edgeBorders(active, stroke, world):
#    if active:
#        if CamX == 0:
#            pg.draw.rect(win, CellClr, (0,0,stroke,CamH*CellWH + GoLPosY*2))
#        if CamX == world.shape[0] - CamW:
#            pg.draw.rect(win, CellClr, (CamW*CellWH + GoLPosX,0,stroke,CamH*CellWH + GoLPosY*2))
#        if CamY == 0:
#            pg.draw.rect(win, CellClr, (0,0,CamH*CellWH + GoLPosY*2,stroke))
#        if CamY == world.shape[1] - CamH:
#            pg.draw.rect(win, CellClr, (0,CamH*CellWH + GoLPosY,CamH*CellWH + GoLPosY*2,stroke))
#
#def winMenu(pos, stroke):
#    global winMenuState
#    # margin
#    pg.draw.rect(win, BgClr, (pos[0],pos[1],150,220))
#    # outline # might hardcode it bc useless calculations, stroke arg doesn't look good at other values
#    pg.draw.rect(win, CellClr, (pos[0]+stroke, pos[1]+stroke, 150-(stroke*2), 220-(stroke*2)))
#    pg.draw.rect(win, BgClr, (pos[0] + (stroke*1.5), pos[1] + (stroke*1.5), 150 - (stroke * 3), 220 - (stroke * 3)))
#    #print(pos)
#
#
#Winrun = True
#GoLPhase = "simu"
#while Winrun:
#    frameCount = frameCount + 1
#    pg.time.delay(800) # 33ms ~= 30fps | 16ms ~= 60fps | multi-threading and gpu accel to be made, might not be needed
#    if pg.event.get(pg.QUIT):
#        Winrun = False
#
#    # if alt then keyIn else keyOn*
#
#    if (pg.event.get(pg.KEYDOWN) if pg.key.get_pressed()[pg.K_LALT] else pg.key.get_pressed()):
#        if pg.key.get_pressed()[pg.K_RIGHT]:
#            CamX += 1
#        if pg.key.get_pressed()[pg.K_LEFT]:
#            CamX -= 1
#        if pg.key.get_pressed()[pg.K_UP]:
#            CamY -= 1
#        if pg.key.get_pressed()[pg.K_DOWN]:
#            CamY += 1
#
#
#    # keyOn
#    if pg.event.get(pg.KEYDOWN):
#        if pg.key.get_pressed()[pg.K_SPACE]:
#            GoLPhase = "edit" if GoLPhase == "simu" else "simu"
#            #if GoLPhase == "edit":
#            #    GoLPhase = "simu"
#            #    print("edit -> simu")
#            #elif GoLPhase == "simu":
#            #    GoLPhase = "edit"
#            #    print("simu -> edit")
#        if pg.key.get_pressed()[pg.K_t]:
#            BgClr = CellClrDef if BgClr == BgClrDef else BgClrDef
#            CellClr = BgClrDef if CellClr == CellClrDef else CellClrDef
#
#    #CamX = mandragore.clamp(CamX, 0, World.shape[1])
#    #CamY = mandragore.clamp(CamY, 0, World.shape[0])
#    #print(CamX,CamY)
#
#
#    #if pg.event.get(pg.MOUSEBUTTONUP):
#    if pg.mouse.get_pressed()[2] and winMenuState == False:
#        #print(pg.event.get(pg.MOUSEBUTTONUP))
#        winMenuState = True
#        winMenuPos = pg.mouse.get_pos()
#    #if pg.mouse.get_pressed()[1] and winMenuState == True:
#
#    if pg.mouse.get_pressed()[0]:
#        #print(pg.mouse.get_pos(), winMenuPos)
#        if winMenuState:
#            if (pg.mouse.get_pos()[0] > winMenuPos[0] + 150 or pg.mouse.get_pos()[0] < winMenuPos[0]) or (pg.mouse.get_pos()[1] < winMenuPos[1] or pg.mouse.get_pos()[1] > winMenuPos[1] + 220):
#                winMenuState = False
#        else:
#            CamX += (winPrevMousePos[0] - pg.mouse.get_pos()[0]) / 16
#            CamY += (winPrevMousePos[1] - pg.mouse.get_pos()[1]) / 16
#
#            # at the end to be used for the next frame
#            winPrevMousePos = pg.mouse.get_pos()
#    else:
#        winPrevMousePos = pg.mouse.get_pos()
#
#    life.evolve()
#    World = life.getlife()
#
#
#    if GoLPhase == "edit":
#        aparecium(StartWorld)
#    if GoLPhase == "simu":
#        aparecium(World)
#        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)
#
#    edgeBorders(True, 4, World)
#
#
#    if winMenuState:
#        winMenu(winMenuPos, 4)
#
#
#    pg.display.update()
#    print("Frame:", frameCount, "World Size:", World.shape, "Camera Position:", CamX, CamY, "taille de globale", life.global_current_life.shape)
#
#pg.quit()