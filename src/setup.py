import pygame
import sys
from exceptions import *

def argParse():
    try:
        if(not (2 < len(sys.argv) < 5)):
            raise InvalidArgCount()
        elif len(sys.argv) == 4:
            canvasWidth = int(sys.argv[1])
            canvasHeight = int(sys.argv[2])
            timeToRun = int(sys.argv[3])
        else:
            canvasWidth = int(sys.argv[1])
            canvasHeight = int(sys.argv[2])
            timeToRun = "Infinite"
    except InvalidArgCount:
        print("Error, correct usage is python3 main.py width height, time limit")
        exit(0)
    except ValueError:
        print("Error, only ints are accepted for width, height and time limit")
        exit(0)

    return canvasWidth, canvasHeight, timeToRun

def pygameSetup(canvasWidth, canvasHeight):

    boxHeight = canvasHeight * .083333333
    boxWidth = canvasWidth * .75
    boxStartX = canvasWidth *.5 - canvasWidth * .75 *.5
    boxStartY = canvasHeight * .166666667

    canvas = pygame.display.set_mode((canvasWidth, canvasHeight))
    
    font = pygame.font.Font(None, int(boxHeight/2))
    
    clock = pygame.time.Clock()

    return canvas, font, clock, boxHeight, boxWidth, boxStartX, boxStartY

def boxSetup(boxStartX, boxStartY, boxWidth, boxHeight):


    inputBox = pygame.Rect(boxStartX, boxStartY+ 2*boxHeight, boxWidth, boxHeight)

    wordBox = pygame.Rect(boxStartX, boxStartY, boxWidth, boxHeight)
    
    inactiveColor = pygame.Color('lightskyblue3')
    activeColor = pygame.Color('dodgerblue2')

    return inputBox, wordBox, inactiveColor, activeColor

def timerSetup():
    pass
