from math import *
import numpy as np
import pygame.image

import lumos
import maraudersMap as backend
import pygame as pg

import wandShop
from wandShop import *


pg.init()
#win = pg.display.set_mode((1280,720))



###################################################### Variables ######################################################

    ## v Preinit vars v ##

BorderW = 4 # pos of the sim on the win
BorderH = 4

GolW = 512
GolH = 512

WorldW = 128
WorldH = 128

    ## v Win init v ##

win = pg.display.set_mode((GolW + BorderW * 2, GolH + BorderH * 2))
pg.display.set_icon(pygame.image.load('icon.png'))
pg.display.set_caption("BC & K6 | Game of Life")
pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)

    ## v WinMenu v ##

winPrevMousePos = pg.mouse.get_pos()
winMenuState = False
winMenuPos = (0,0)
winMenuSize = (150,220)
winMenuStroke = 4
winMenuElements = []

    ## v MouseEvents v ##

mouseIn = [False,False,False] # 0=L 1=M 2=R
mouseOut = [False,False,False]
mouseOnLastFrame = [False,False,False]
mouseOn = [False,False,False]

    ## v Customizable v ##

FrameRate = 60

CellSize = 8 # Zoom, in a way
CellClr = CellClrDef = (255,255,255)
BgClr = BgClrDef = (0,0,0)

SimSpeed = 2

#MouseSensitivity = 1

    ## v Other v ##

CamX = 0
CamY = 0
CamW = int(GolW / CellSize)
CamH = int(GolH / CellSize)

FrameCount = 0
FrameMS = int(1/FrameRate*1000)

    ## v Preload v ##

pauseImg = pg.image.load("textures/actions/pause.png")
playImg = pg.image.load("textures/actions/play.png")
speedImg = pg.image.load("textures/actions/speed.png")
zoomImg = pg.image.load("textures/actions/zoom.png")
editImg = pg.image.load("textures/actions/edit.png")

dillan = pg.font.SysFont("Dillan", 16)

pauseLbl = dillan.render("Pause [Toggle]", True, (255, 255, 255))
playLbl = dillan.render("Play [Toggle]", True, (255, 255, 255))
speedLbl = dillan.render("Speed [Slider]", True, (255, 255, 255))
zoomLbl = dillan.render("Zoom [Slider]", True, (255, 255, 255))
editLbl = dillan.render("Edit [Toggle]", True, (255, 255, 255))
simLbl = dillan.render("Simulate [Toggle]", True, (255, 255, 255))





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
    if world.shape[0] < GolW/CellSize or world.shape[1] < GolH/CellSize:
        pg.draw.rect(win, CellClr, (0,0, stroke,world.shape[1]*CellSize + BorderH*2))
        pg.draw.rect(win, CellClr, (world.shape[0]*CellSize + BorderW+stroke,0, stroke,world.shape[1]*CellSize + BorderH*2))
        pg.draw.rect(win, CellClr, (0,0, world.shape[0]*CellSize + BorderW*2,stroke))
        pg.draw.rect(win, CellClr, (0,world.shape[1]*CellSize + BorderH+stroke, world.shape[0]*CellSize + BorderW*2, stroke))
    else:
        if CamX <= stroke/CellSize:
            pg.draw.rect(win, CellClr, (0,0, stroke,GolH+BorderH*2))
        if CamX >= world.shape[0] - CamW - stroke/CellSize:
            pg.draw.rect(win, CellClr, (GolW + BorderW*2 - stroke,0, stroke,GolH+BorderH*2))
        if CamY <= stroke/CellSize:
            pg.draw.rect(win, CellClr, (0,0, GolW+BorderW*2,stroke))
        if CamY >= world.shape[1] - CamH - stroke/CellSize:
            pg.draw.rect(win, CellClr, (0,GolH+BorderH*2-stroke, GolW+BorderW*2,stroke))



def winMenuInit():
    global winMenuElements, winMenuSize, winMenuStroke
    size = winMenuSize
    stroke = winMenuStroke
    margin = 4
    origin = stroke*2

    pause = wandShop.CollisionZone([origin + margin, origin + margin + ((16 + margin) * len(winMenuElements))],
                                   [size[0] - 2 * (origin + margin), 16])
    winMenuElements.append(pause)


    speed = wandShop.CollisionZone([origin + margin, origin + margin + ((16 + margin) * len(winMenuElements))],
                                   [size[0] - 2 * (origin + margin), 16])
    winMenuElements.append(speed)


    zoom = wandShop.CollisionZone([origin + margin, origin + margin + ((16 + margin) * len(winMenuElements))],
                                   [size[0] - 2 * (origin + margin), 16])
    winMenuElements.append(zoom)


    edit = wandShop.CollisionZone([origin + margin, origin + margin + ((16 + margin) * len(winMenuElements))],
                                   [size[0] - 2 * (origin + margin), 16])
    winMenuElements.append(edit)


def winMenu():
    global winMenuElements, winMenuState, winMenuSize, winMenuStroke, winMenuPos, SimRun, SimSpeed, CellSize, CamW, CamH
    elements = winMenuElements
    size = winMenuSize
    stroke = winMenuStroke
    pos = np.array(winMenuPos)
    #origin = stroke*2

    #mPos = np.array(pos) # = mutablePos, can't do math on tuples bc they're "immutable"
    #dillan = pg.font.SysFont("Dillan", 16)

    # margin
    pg.draw.rect(win, BgClr, (pos[0],pos[1],size[0],size[1]))

    # outline # might hardcode it bc useless calculations, stroke arg doesn't look good at other values
    pg.draw.rect(win, CellClr, (pos[0]+stroke, pos[1]+stroke, size[0]-(stroke*2), size[1]-(stroke*2)))
    pg.draw.rect(win, BgClr, (pos[0] + (stroke*1.5), pos[1] + (stroke*1.5), size[0] - (stroke * 3), size[1] - (stroke * 3)))


    for element in range(len(elements)):
        if elements[element].isHovered(pg.mouse.get_pos(),pos):
            pg.draw.rect(win, (64,64,64), (elements[element].getPos() + pos, elements[element].getSize()))
            if element == 0:
                if mouseOut[0]:
                    SimRun = wandShop.switch(SimRun)

            if element == 1:
                if mouseOut[0]:
                    SimSpeed = clamp(SimSpeed/2, 0, 1)
                if mouseOut[2]:
                    SimSpeed = clamp(SimSpeed*2, 0, 1)

            if element == 2:
                if mouseOut[0]:
                    CellSize += 1
                    CamW = int(GolW / CellSize)
                    CamH = int(GolH / CellSize)
                    print("Zoom:", CellSize)
                if mouseOut[2]:
                    CellSize -= 1
                    CellSize = wandShop.clamp(CellSize,1)
                    CamW = int(GolW / CellSize)
                    CamH = int(GolH / CellSize)
                    print("Zoom:", CellSize)

    # actions
    fontOffsetY = 3

    if SimRun:
        win.blit(pauseImg, elements[0].getPos() + pos)
        win.blit(pauseLbl, (elements[0].getPos()[0] + 16 + stroke + pos[0],
                            elements[0].getPos()[1] + pos[1] + fontOffsetY))
    else:
        win.blit(playImg, elements[0].getPos() + pos)
        win.blit(playLbl, (elements[0].getPos()[0] + 16 + stroke + pos[0],
                           elements[0].getPos()[1] + pos[1] + fontOffsetY))

    win.blit(speedImg, elements[1].getPos() + pos)
    win.blit(speedLbl, (elements[1].getPos()[0] + 16 + stroke + pos[0],
                        elements[1].getPos()[1] + pos[1] + fontOffsetY))

    win.blit(zoomImg, elements[2].getPos() + pos)
    win.blit(zoomLbl, (elements[2].getPos()[0] + 16 + stroke + pos[0],
                        elements[2].getPos()[1] + pos[1] + fontOffsetY))


def init():
    winMenuInit()

init()

Winrun = True
SimRun = True
while Winrun:
    pg.time.delay(16) # 33ms ~= 30fps | 16ms ~= 60fps | multi-threading and gpu accel to be made, might not be needed
    if pg.event.get(pg.QUIT):
        Winrun = False


    for buttons in [0,1,2]:
        if pg.mouse.get_pressed()[buttons]:
            mouseOn[buttons] = True
            if not mouseOnLastFrame[buttons]:
                mouseIn[buttons] = True
                #print(mouseIn[buttons])
            elif mouseIn[buttons]:
                mouseIn[buttons] = False
                #print(mouseIn[buttons])
        else:
            mouseOn[buttons] = False
            if mouseOnLastFrame[buttons]:
                mouseOut[buttons] = True
                #print(mouseOut[buttons])
            elif mouseOut[buttons]:
                mouseOut[buttons] = False
                #print(mouseOut[buttons])
    mouseOnLastFrame = pg.mouse.get_pressed()
    #print(mouseIn,mouseOut,mouseOnLastFrame)



    # if alt then keyIn else keyOn
    if pg.event.get(pg.KEYDOWN) if pg.key.get_pressed()[pg.K_LALT] else pg.key.get_pressed():
        # if the simulation is unzoomed enough to be able to move
        if World.shape[0] > GolW / CellSize and World.shape[1] > GolH / CellSize:
            CamX += (int(pg.key.get_pressed()[pg.K_RIGHT]) - int(pg.key.get_pressed()[pg.K_LEFT]))
            CamY += (int(pg.key.get_pressed()[pg.K_DOWN]) - int(pg.key.get_pressed()[pg.K_UP])) #* int(120 / FrameRate)

    # keyIn
    if pg.event.get(pg.KEYDOWN):
        if pg.key.get_pressed()[pg.K_SPACE]:
            #GoLPhase = "edit" if GoLPhase == "simu" else "simu"
            SimRun = switch(SimRun)
        if pg.key.get_pressed()[pg.K_t]:
            # swap
            BgClr = CellClrDef if BgClr == BgClrDef else BgClrDef
            CellClr = BgClrDef if CellClr == CellClrDef else CellClrDef


    # show winMenu on RClickOut
    if mouseOut[2] and winMenuState == False:
        winMenuState = True
        winMenuPos = np.array(pg.mouse.get_pos())
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    # unfocus winMenu or move
    if pg.mouse.get_pressed()[0]:
        if winMenuState:
            if (pg.mouse.get_pos()[0] > winMenuPos[0] + 150 or pg.mouse.get_pos()[0] < winMenuPos[0]) or (pg.mouse.get_pos()[1] < winMenuPos[1] or pg.mouse.get_pos()[1] > winMenuPos[1] + 220):
                winMenuState = False
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)
        else:
            if World.shape[0] > GolW / CellSize and World.shape[1] > GolH / CellSize:
                CamX += (winPrevMousePos[0] - pg.mouse.get_pos()[0]) / CellSize #/ MouseSensitivity
                CamY += (winPrevMousePos[1] - pg.mouse.get_pos()[1]) / CellSize

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
        FrameCount += 1
        if FrameCount >= 1/SimSpeed: # will change
            life.evolve()
            World = life.getlife()
            FrameCount = 0
        # debug
        #print("Frame:", FrameCount, "World Size:", World.shape, "Camera Position:", CamX, CamY, "taille du monde",
        #      life.global_shape)

    aparecium(World)
    print(CamX,CamY, CamW, CamH)

    # applied every frame will get rid of eventually actually ima do it now so if u still see this line well idk must have gotten lazy
    #if GoLPhase == "edit":
    #    aparecium(StartWorld)
    #if GoLPhase == "sim":


    # ITS IN DA NAME FFS U RLY NEED A COMMENT FOR DIS
    if True:
        edgeBorders(2, World)

    # defer winMenu() to after everything else, position in the code acts as z-index
    if winMenuState:
        winMenu()
        #print(winMenuElements[0].isHovered(pg.mouse.get_pos(),winMenuPos))

    # update the whole screen
    pg.display.update()

pg.quit()