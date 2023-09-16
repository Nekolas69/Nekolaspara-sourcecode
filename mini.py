import pygame
import time
pygame.init()
pygame.mixer.init()
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
instruct = False
pause = False
missed_sound = pygame.mixer.Sound("les/missed.mp3")
succes_sound = pygame.mixer.Sound("les/success.mp3")
def drawBlock(x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
def drawBlocks(x, y, width, height):
    pygame.draw.rect(screen, red, (x, y-40, width, height))
def drawBlockk(x, y, width, height):
    pygame.draw.rect(screen, white, (x, y, width, height))
def kacenihra():
    global pause
    game = True
    firstBlock_w = 400
    firstBlock_h = 40
    firstBlock_x = WIDTH / 2  -300
    firstBlock_y = 525
    block_w = 400
    block_h = 40
    changing_block_x = WIDTH / 2 - firstBlock_w / 2
    changing_block_y = 525
    changing_block_dx = 0
    move_right = True
    speed = 5
    score = 0
    tries = 5
    while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if changing_block_x >= firstBlock_x-15 and changing_block_x+block_w <= firstBlock_x+block_w+15:
                            speed += 1
                            score += 1
                            pygame.mixer.Sound.play(succes_sound)
                            time.sleep(0.5)
                        else:
                            pygame.mixer.Sound.play(missed_sound)
                            time.sleep(0.5)
            changing_block_x += changing_block_dx
            screen.fill(black)
            if changing_block_x+firstBlock_w > WIDTH:
                move_right = False
            elif changing_block_x < 0:
                move_right = True
            if move_right:
                changing_block_dx = speed
            elif not move_right:
                changing_block_dx = -speed
            if score%13 == 0:
                firstBlock_h = 40
                firstBlock_y = 525
                changing_block_y = 525
            if score>=20:break
            nebe=pygame.transform.scale(pygame.image.load("les/les2.jpg"),(WIDTH,HEIGHT))
            screen.blit(nebe, (0, 0))
            drawBlocks(changing_block_x, changing_block_y, block_w, block_h)
            pygame.display.update()
            clock.tick(FPS)