from math import *
import numpy as np
import pygame.image

import lumos
import maraudersMap as backend
import pygame as pg
from util import *


pg.init()



###################################################### Variables ######################################################

    ## v Preinit vars v ##

BorderW = 4 # pos of the sim on the win
BorderH = 4

WinW = 512
WinH = 512

WorldW = 128
WorldH = 128

    ## v Win init v ##

win = pg.display.set_mode((WinW + BorderW * 2, WinH + BorderH * 2))
pg.display.set_icon(pygame.image.load('icon.png'))
pg.display.set_caption("GoL")
pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)

    ## v WinMenu v ##

winPrevMousePos = pg.mouse.get_pos()
winMenuState = False
winMenuPos = (0,0)

    ## v Other v ##

CellSize = 8 # Zoom, in a way
CellClr = CellClrDef = (255,255,255)
BgClr = BgClrDef = (0,0,0)

CamX = 0
CamY = 0
CamW = int(WinW / CellSize)
CamH = int(WinH / CellSize)

frameCount = 0



######################################################### Core #########################################################

life = backend.Life((WorldW, WorldH))
life.draw_adapt('canadagoose', (0,0), rotation=2)
World = life.getlife()



def aparecium(world):
    global CamX, CamY
    CamX = clamp(CamX, 0, World.shape[0] - CamW)
    CamY = clamp(CamY, 0, World.shape[1] - CamH)
    View = np.array(world[floor(CamY):floor(CamY)+CamH,floor(CamX):floor(CamX)+CamW])
    
    win.fill(BgClr) # fill black / reset
    
    view_cordantate = np.array(np.where(View == 1)).tolist()
    for cy, cx in zip(view_cordantate[0],view_cordantate[1]):
        pg.draw.rect(win, CellClr, (cx * CellSize + BorderW, cy * CellSize + BorderH, CellSize, CellSize))



def edgeBorders(stroke, world):
    if world.shape[0] < WinW/CellSize or world.shape[1] < WinH/CellSize:
        pg.draw.rect(win, CellClr, (0,0, stroke,world.shape[1]*CellSize + BorderH*2))
        pg.draw.rect(win, CellClr, (world.shape[0]*CellSize + BorderW+stroke,0, stroke,world.shape[1]*CellSize + BorderH*2))
        pg.draw.rect(win, CellClr, (0,0, world.shape[0]*CellSize + BorderW*2,stroke))
        pg.draw.rect(win, CellClr, (0,world.shape[1]*CellSize + BorderH+stroke, world.shape[0]*CellSize + BorderW*2, stroke))
    else:
        if CamX <= stroke:
            pg.draw.rect(win, CellClr, (0,0, stroke,WinH+BorderH*2))
        if CamX >= world.shape[0] - CamW - stroke:
            pg.draw.rect(win, CellClr, (WinW + BorderW*2 - stroke,0, stroke,WinH+BorderH*2))
        if CamY <= stroke:
            pg.draw.rect(win, CellClr, (0,0, WinW+BorderW*2,stroke))
        if CamY >= world.shape[1] - CamH - stroke:
            pg.draw.rect(win, CellClr, (0,WinH+BorderH*2-stroke, WinW+BorderW*2,stroke))




def winMenu(pos, stroke):
    global winMenuState
    mPos = np.array(pos) # = mutablePos, can't do math on tuples bc they're "immutable"
    dillan = pg.font.SysFont("Dillan", 16)

    # margin
    pg.draw.rect(win, BgClr, (pos[0],pos[1],150,220))

    # outline # might hardcode it bc useless calculations, stroke arg doesn't look good at other values
    pg.draw.rect(win, CellClr, (pos[0]+stroke, pos[1]+stroke, 150-(stroke*2), 220-(stroke*2)))
    pg.draw.rect(win, BgClr, (pos[0] + (stroke*1.5), pos[1] + (stroke*1.5), 150 - (stroke * 3), 220 - (stroke * 3)))

    # buttons

    ## Play/Pause
    buttonNumber = 0
    prev = pg.image.load("textures/actions/pause.png")
    win.blit(prev, mPos+(stroke*3,stroke*3 + buttonNumber*16))
    prevLbl = dillan.render("Pause", True, (255,255,255))
    win.blit(prevLbl,mPos+(stroke*4 + 16,stroke*3 + 3 + buttonNumber*16)) # 3=distance from top | 2=inBetweenMargin

    buttonNumber = 1
    speed = pg.image.load("textures/actions/speed.png")
    win.blit(speed, mPos + (stroke*3, stroke*3 + 2 + buttonNumber*16))
    speedLbl = dillan.render("Speed [Slider]", True, (255, 255, 255))
    win.blit(speedLbl, mPos + (stroke*4 + 16, stroke*3 + 3 + 2 + buttonNumber*16))



Winrun = True
GoLPhase = "sim"
SimRun = True
while Winrun:
    pg.time.delay(8) # 33ms ~= 30fps | 16ms ~= 60fps | multi-threading and gpu accel to be made, might not be needed
    if pg.event.get(pg.QUIT):
        Winrun = False

    # if alt then keyIn else keyOn
    if pg.event.get(pg.KEYDOWN) if pg.key.get_pressed()[pg.K_LALT] else pg.key.get_pressed():
        CamX += int(pg.key.get_pressed()[pg.K_RIGHT]) - int(pg.key.get_pressed()[pg.K_LEFT])
        CamY += int(pg.key.get_pressed()[pg.K_DOWN]) - int(pg.key.get_pressed()[pg.K_UP])

    # keyIn
    if pg.event.get(pg.KEYDOWN):
        if pg.key.get_pressed()[pg.K_SPACE]:
            #GoLPhase = "edit" if GoLPhase == "simu" else "simu"
            SimRun = switch(SimRun)
        if pg.key.get_pressed()[pg.K_t]:
            # swap
            BgClr = CellClrDef if BgClr == BgClrDef else BgClrDef
            CellClr = BgClrDef if CellClr == CellClrDef else CellClrDef


    # show winMenu on RClick
    if pg.mouse.get_pressed()[2] and winMenuState == False:
        winMenuState = True
        winMenuPos = pg.mouse.get_pos()

    # unfocus winMenu or move
    if pg.mouse.get_pressed()[0]:
        if winMenuState:
            if (pg.mouse.get_pos()[0] > winMenuPos[0] + 150 or pg.mouse.get_pos()[0] < winMenuPos[0]) or (pg.mouse.get_pos()[1] < winMenuPos[1] or pg.mouse.get_pos()[1] > winMenuPos[1] + 220):
                winMenuState = False
        else:
            CamX += (winPrevMousePos[0] - pg.mouse.get_pos()[0]) / 16
            CamY += (winPrevMousePos[1] - pg.mouse.get_pos()[1]) / 16

            # at the end to be used for the next frame
            winPrevMousePos = pg.mouse.get_pos()
    else:
        winPrevMousePos = pg.mouse.get_pos()
    if pg.mouse.get_pressed()[2]:
        if winMenuState:
            if (pg.mouse.get_pos()[0] > winMenuPos[0] + 150 or pg.mouse.get_pos()[0] < winMenuPos[0]) or (pg.mouse.get_pos()[1] < winMenuPos[1] or pg.mouse.get_pos()[1] > winMenuPos[1] + 220):
                winMenuState = False



    # calc next frame
    if SimRun:
        life.evolve()
        World = life.getlife()
        frameCount += 1
        # debug
        print("Frame:", frameCount, "World Size:", World.shape, "Camera Position:", CamX, CamY, "taille du monde",
              life.global_shape)

    aparecium(World)

    # applied every frame will get rid of eventually actually ima do it now so if u still see this line well idk must have gotten lazy
    #if GoLPhase == "edit":
    #    aparecium(StartWorld)
    #if GoLPhase == "sim":


    # ITS IN DA NAME FFS U RLY NEED A COMMENT FOR DIS
    if True:
        edgeBorders(2, World)

    # defer winMenu() to after everything else, position in the code acts as z-index
    if winMenuState:
        winMenu(winMenuPos, 4)

    # vvv WOW DIS IS IMPORTANT HEY LOOK ITS RIGHT FKIN HERE vvv
    pg.display.update()
    # ^^^ SAW IT NAH TOO BAD U MISSED IT BRAINDEAD DUMBA- ^^^


pg.quit()
