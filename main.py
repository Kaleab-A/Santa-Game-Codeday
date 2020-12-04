import pygame
import random

# Initalizing Pygame
pygame.init();
scrWidth = 1024
scrHeight = 512

# Create the Screen
win = pygame.display.set_mode((scrWidth, scrHeight))

pygame.display.set_caption("First Game")

# Loading Image
walkRight = []
walkLeft = []
for i in range(1, 14):
    path = ".//santasprites//png//Walk//"
    name = "Walk (" + str(i) + ").png"
    picture = pygame.image.load(path + name)
    picture = pygame.transform.scale(picture, (186, 128))
    pictureFlip = pygame.transform.flip(picture, True, False)
    walkRight.append(picture)
    walkLeft.append(pictureFlip)
bg = pygame.image.load(".//Images//wintertileset//png//BG//BG.png")
bg = pygame.transform.scale(bg, (scrWidth, scrHeight))
ground1, ground2, ground3 = pygame.image.load(".//Images//wintertileset//png//Tiles//1.png"), pygame.image.load(".//Images//wintertileset//png//Tiles//2.png"), pygame.image.load(".//Images//wintertileset//png//Tiles//3.png")
ground4, ground5, ground6 = pygame.image.load(".//Images//wintertileset//png//Tiles//4.png"), pygame.image.load(".//Images//wintertileset//png//Tiles//5.png"), pygame.image.load(".//Images//wintertileset//png//Tiles//6.png"), 
ground1 = pygame.transform.scale(ground1, (64, 64))
ground2 = pygame.transform.scale(ground2, (64, 64))
ground3 = pygame.transform.scale(ground3, (64, 64))
ground4 = pygame.transform.scale(ground4, (64, 64))
ground5 = pygame.transform.scale(ground5, (64, 64))
ground6 = pygame.transform.scale(ground6, (64, 64))
water1, water2 = pygame.image.load(".//Images//wintertileset//png//Tiles//17.png"), pygame.image.load(".//Images//wintertileset//png//Tiles//18.png")
water1 = pygame.transform.scale(water1, (64, 64))
water2 = pygame.transform.scale(water2, (64, 64))
charR = pygame.transform.scale(pygame.image.load(".//santasprites//png//Idle/Idle (1).png"), (186, 128))
charL = pygame.transform.flip(charR, True, False)
clock = pygame.time.Clock()
color = {"black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0)}


class Player (object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        self.isJump = False
        self.initJumpCount = 10
        self.jumpCount = self.initJumpCount
        self.jumpConst = 0.5
        self.left = False
        self.right = False
        self.idle = True
        self.walkCount = 0

    def draw(self, win):
        if self.walkCount + 1 > 13*3: self.walkCount = 0
        if self.idle:
            if self.left: win.blit(charL, (self.x, self.y))
            else: win.blit(charR, (self.x, self.y))
        elif self.isJump:
            if self.left: win.blit(charL, (self.x, self.y))
            else: win.blit(charR, (self.x, self.y))
        elif self.left: win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
        elif self.right: win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
        else: assert 1

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = round(x)
        self.y = round(y)
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius )


playerMain = Player(scrWidth//2, scrHeight-190, 93, 64)
running = True
count = [0]
groundLevel = []
def drawGround():
    if groundLevel == []:
        prevLevel = 3
        groundLevel.append(prevLevel)
        nextLevel = prevLevel
        while len(groundLevel) < scrWidth // 64:
            nextLevel = random.randint(max(0, prevLevel-3),  prevLevel + 2)
            groundLevel.append(nextLevel)
            if nextLevel != prevLevel:
                groundLevel.append(nextLevel)
            prevLevel = nextLevel
        print(groundLevel)

    index = 0
    for i in range(0, scrWidth, 64):
        if groundLevel[index] == 0:
            win.blit(water1, (i, scrHeight-64))
        elif index != len(groundLevel) -1 and groundLevel[index] > groundLevel[index+1]:
            win.blit(ground3, (i, scrHeight-(64*groundLevel[index])))
        elif index != 0 and groundLevel[index] > groundLevel[index-1]:
            win.blit(ground1, (i, scrHeight-(64*groundLevel[index])))
        else:
            win.blit(ground2, (i, scrHeight-(64*groundLevel[index])))
        for j in range(0, 64*groundLevel[index], 64):
            win.blit(ground5, (i, scrHeight-j))
        index += 1


    # for i in range(64, scrWidth-64, 64):
    #     win.blit(ground2, (i, scrHeight-128))
    # win.blit(ground1, (0, scrHeight-128))
    # win.blit(ground3, (i+64, scrHeight-128))

    # for i in range(64, scrWidth-64, 64):
    #     win.blit(ground5, (i, scrHeight-64))
    # win.blit(ground4, (0, scrHeight-64))
    # win.blit(ground6, (i+64, scrHeight-64))

def redrawGameWindow():
    # win.fill((198, 198, 198))
    win.blit(bg, (0, 0))
    drawGround()
    playerMain.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    count[0] += 1
    pygame.display.update()

bullets = []
while running:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if playerMain.left: facing = -1
                else: facing = 1
                if len(bullets) < 10:
                    bullets.append(projectile((2*playerMain.x + playerMain.width)//2,  (2*playerMain.y + playerMain.height)//2, 6, color["red"], facing))

    newBullets = []
    for index in range(len(bullets)):
        bullet = bullets[index]
        if bullet.x  < scrWidth and bullet.x > 0:
            bullet.x += bullet.velocity
            newBullets.append(bullet)  

    bullets = newBullets.copy()      
    keys = pygame.key.get_pressed()

    

    if keys[pygame.K_LEFT] and playerMain.x >= playerMain.velocity:
        playerMain.x -= playerMain.velocity
        playerMain.left, playerMain.right, playerMain.idle = True, False, False
        playerMain.walkCount += 1
    elif keys[pygame.K_RIGHT] and playerMain.x <= scrWidth - playerMain.width - playerMain.velocity:
        playerMain.x += playerMain.velocity
        playerMain.left, playerMain.right, playerMain.idle = False, True, False
        playerMain.walkCount += 1
    else:
        playerMain.walkCount = 0
        playerMain.idle = True

    if not playerMain.isJump:
        if keys[pygame.K_UP]:
            playerMain.isJump = True
    if playerMain.isJump:
        if playerMain.jumpCount >= -playerMain.initJumpCount:
            playerMain.jumpAmount = (playerMain.jumpCount ** 2) * playerMain.jumpConst
            if playerMain.jumpCount < 0:
                playerMain.y += playerMain.jumpAmount
            else:
                playerMain.y -= playerMain.jumpAmount
            playerMain.jumpCount -= 1
        else:
            playerMain.isJump = False
            playerMain.jumpCount = playerMain.initJumpCount

    redrawGameWindow()

pygame.quit()

