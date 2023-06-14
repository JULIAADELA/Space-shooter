import math
import random

from pygame import mixer
from button import *

# initialise pygame
pygame.init()
# set frame rate
clock = pygame.time.Clock()

# game window
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Sound
mixer.music.load('sounds/music.wav')
laser_sound = mixer.Sound('sounds/laser.wav')
boom_sound = mixer.Sound('sounds/boom.wav')
mixer.music.play(-1)

# define font
score_font = pygame.font.SysFont('comicsansms', 35)
over_font = pygame.font.SysFont('comicsansms', 100)

# load images
background = pygame.image.load('bg/background.png')
ship = pygame.image.load('spaceship.png')
bullet_img = pygame.image.load('laser.png')

# start game
g = GameIntro()
g.menu()
g.instruction()

# Space ship
def Ship(x, y):
    screen.blit(ship, (x, y))

# Enemy
enemyImg= []
enemy_list = ['enemy/1.png','enemy/2.png','enemy/3.png','enemy/4.png','enemy/5.png',
              'enemy/7.png','enemy/8.png','enemy/6.png','enemy/9.png']
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(10):
    for image in enemy_list:
        enemyImg.append(pygame.image.load(image))
    enemyX.append(random.randint(5, 750))
    enemyY.append(random.randint(50, 90))
    enemyX_change.append(4)
    enemyY_change.append(20)
def Enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
# Bullet
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 20
bullet = "ready"   # You can't see the bullet on the screen
def Shoot_bullet(x, y):
    global bullet
    bullet = "go"  # The bullet is currently moving
    screen.blit(bullet_img, (x + 30, y + 10))

def Coll(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 50:
        return True
    else:
        return False

# Score
score_value = 0
def Show_score(x, y):
    score = score_font.render('Score : ' + str(score_value), True, GREEN)
    screen.blit(score,(x, y))

def Game_over():
    over_text = over_font.render('GAME OVER', True, RED)
    screen.blit(over_text, (130, 150))
    text = score_font.render(f'Your score is {str(score_value)}. You want to play again',True,WHITE)
    screen.blit(text,(120,290))

# Game Loop
ship_x = 380
ship_y = 550
speedX = 0
speedY = 0
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    # Background Image
    screen.blit(background, (0, 0))
    # limit ship movement
    ship_x += speedX
    ship_y += speedY
    if ship_x <= 0:
        ship_x = 0
    elif ship_x >= 760:
        ship_x = 760
    if ship_y <= 0:
        ship_y = 0
    if ship_y >= 550:
        ship_y = 550
    # ship move
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right, left, up, down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speedX = -5
            if event.key == pygame.K_RIGHT:
                speedX = 5
            if event.key == pygame.K_UP:
                speedY = -5
            if event.key == pygame.K_DOWN:
                speedY = 5
            if event.key == pygame.K_SPACE:
                if bullet == "ready":
                    laser_sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = ship_x
                    bulletY = ship_y
                    Shoot_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                speedX = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                speedY = 0
    # Bullet Movement
    if bulletY <= 0:
        bullet = "ready"
    if bullet == "go":
        Shoot_bullet(bulletX, bulletY)
        bulletX -= bulletX_change
        bulletY -= bulletY_change
    # Enemy Movement
    for i in range(10):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 760:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = Coll(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            boom_sound.play()
            bullet = "go"
            score_value += 1
            enemyX[i] = random.randint(5, 760)
            enemyX[i] = random.randint(50, 90)
        Enemy(enemyX[i], enemyY[i], i)
        # Game Over
        if enemyY[i] > 500:
            for j in range(10):
                enemyY[j] = 1000
            Game_over()
            break

    Ship(ship_x,ship_y)
    Show_score(0,0)
    pygame.display.update()
pygame.quit()
