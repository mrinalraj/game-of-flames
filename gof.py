#!/usr/bin/env python

import pygame
import random
import sys
from screeninfo import get_monitors
from pygame.locals import *

MONITOR = str(get_monitors()[0])
SYSTEM_RESOLUTION = (MONITOR.split('+'))[0]
WINDOWWIDTH = int(((SYSTEM_RESOLUTION.split('x')[0]).split('('))[1])
WINDOWHEIGHT = int(SYSTEM_RESOLUTION.split('x')[1])
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = pygame.image.load('assets/images/bg.png')
FPS = 120
FIREMINSIZE = 10
FIREMAXSIZE = 40
FIREMINSPEED = 1
FIREMAXSPEED = 8
ADDNEWFIRERATE = 6
PLAYERMOVERATE = 5


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    terminate()
                return


def playerHasHitFire(playerRect, fires):
    for b in fires:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Game of flames')
pygame.mouse.set_visible(True)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('assets/music/gameover.wav')
pygame.mixer.music.load('assets/music/background.mp3')

# set up images
playerImage = pygame.image.load('assets/images/player.png')
playerRect = playerImage.get_rect()
fireImage = pygame.image.load('assets/images/fire.png')

# show the "Start" screen
drawText('Game of flames', font, windowSurface,
         (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface,
         (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    fires = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 200)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    fireAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # the game loop runs while the game part is playing
        score += 1  # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                if event.key == ord('x'):
                    slowCheat = False
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(
                    event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new fires at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            fireAddCounter += 1
        if fireAddCounter == ADDNEWFIRERATE:
            fireAddCounter = 0
            fireSize = random.randint(FIREMINSIZE, FIREMAXSIZE)
            newFire = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-fireSize), 0 - fireSize, fireSize, fireSize),
                       'speed': random.randint(FIREMINSPEED, FIREMAXSPEED),
                       'surface': pygame.transform.scale(fireImage, (fireSize, fireSize)),
                       }

            fires.append(newFire)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the fires down.
        for b in fires:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         # Delete fires that have fallen past the bottom.
        for b in fires[:]:
            if b['rect'].top > WINDOWHEIGHT:
                fires.remove(b)

        # Draw the game world on the window.
        windowSurface.blit(BACKGROUNDCOLOR, (0, 0))

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each fire
        for b in fires:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the fires have hit the player.
        if playerHasHitFire(playerRect, fires):
            if score > topScore:
                topScore = score  # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface,
             (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface,
             (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
