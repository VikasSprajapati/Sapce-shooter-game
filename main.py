import pygame
import random
import math
from pygame import mixer
#intialise the pygame
pygame.init()
clock= pygame.time.Clock()
#create the screen
screen = pygame.display.set_mode((800,600))

#background
background=pygame.image.load('b.png')

#backg sound
mixer.music.load('backg.wav')
mixer.music.play(-1)

#tittle and Icon
pygame.display.set_caption("tufani rocket")
icon= pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


#player
playerimg = pygame.image.load('s.png')
playerX = 370
playerY = 480
playerX_change=0

#Enmey

enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_ofenemies = 10

for i in range(num_ofenemies):

    enemyimg.append(pygame.image.load('kk.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)
    

#bullet

# ready- you can't see the bullet on the screen
# fire- the bullet is currently moving

bulletimg = pygame.image.load('bb.png')
bulletX = 0
bulletY = 480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

#score= 0
score_value=0
font = pygame.font.Font('gg.ttf',32)

textX= 10
testY= 10

#game over text
over_font = pygame.font.Font('gg.ttf',64)



def show_score(x,y):
    score = font.render("score : "+ str(score_value),True,(255,255,255))
    screen.blit(score,  (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,  (200,250))

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16,y+10))

def iscoliision(enemyX,enemyY,bulletX,bulletY):
    distance= math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


# game loop 
running = True
while running:
    
    #RGB = RED, GREEN , BLUE
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if heystroke is pressed cheak whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    #get the current x cordi nate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX ,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    #checking  for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change
    if playerX<= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    # Enemy  movement
    for i in range(num_ofenemies):
        # game over
        if enemyY[i] > 350:
            for j in range(num_ofenemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        
        #collision
        collision= iscoliision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound('expo.wav')
            explosion_sound.play()
            bulletY=480
            bullet_state = "ready"
            score_value += 1
           # print(score)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150) 

        enemy(enemyX[i],enemyY[i],i)

    # bullet movement
    if bulletY <=0:
        bulletY=480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX ,bulletY)
        bulletY -= bulletY_change

    

    player(playerX,playerY)
    show_score(textX,testY)
    pygame.display.update()