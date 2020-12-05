import pygame
import random

# Initalizing Pygame
pygame.init()
scrWidth = 1024
scrHeight = 512
distance = 0
moveSpeed = 10

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
additionalObjects = []
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//Crate.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//Crystal.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//IceBox.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//Igloo.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//Sign_1.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//Sign_2.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//SnowMan.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//Stone.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//Tree_1.png"))
additionalObjects.append(pygame.image.load(".//Images//wintertileset//png//object//Tree_2.png"))
for i in range(len(additionalObjects)):
    additionalObjects[i] = pygame.transform.scale(additionalObjects[i], (64, 64))

charR = pygame.transform.scale(pygame.image.load(".//santasprites//png//Idle/Idle (1).png"), (186, 128))
charL = pygame.transform.flip(charR, True, False)
clock = pygame.time.Clock()
color = {"black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0)}


def offsetBlit(surface, coordinates):
    x, y = coordinates
    win.blit(surface, (x + distance, y))


class Player (object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.constantX = scrWidth // 2
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
        if not self.isJump:
            self.y = scrHeight - groundLevel[self.x // 64 + 1] * 64 - 64 - 50
        print(groundLevel[self.constantX // 64 + 1] )
        if self.walkCount + 1 > 13*3: self.walkCount = 0
        if self.idle:
            if self.left: 
                win.blit(charL, (self.constantX, self.y))
            else: 
                win.blit(charR, (self.constantX, self.y))
        elif self.isJump:
            if self.left: 
                win.blit(charL, (self.constantX, self.y))
            else: 
                win.blit(charR, (self.constantX, self.y))
        elif self.left: 
            win.blit(walkLeft[self.walkCount // 3], (self.constantX, self.y))
        elif self.right: 
            win.blit(walkRight[self.walkCount // 3], (self.constantX, self.y))
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


class enemy(object):
    enemyRight = []
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        # self.left = False
        # self.right = False
        # self.idle = True
        self.end = end
        self.walkCount = 0
        self.path = [self.x, self.end]

    def draw(self, win):
        self.move()
        if self.walkCount + 1 <= 3 * 11:
            self.walkCount = 0


        
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel 
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[1]:
                self.x += self.vel
            else:
                self.walkCount *= -1

playerMain = Player(scrWidth//2, scrHeight-190, 93, 64)
running = True
count = [0]
groundLevel = []
additionalObjectsList = []
def drawGround():
    if groundLevel == []:
        prevLevel = 3
        groundLevel.append(prevLevel)
        nextLevel = prevLevel

        isObjectAdded = random.choices([0, 1], [0.7, 0.3])[0]
        if isObjectAdded:
            additionalObjectsList.append(random.choice(additionalObjects))
        else:
            additionalObjectsList.append(0)

        while len(groundLevel) < scrWidth // 64:
            chance = random.randint(1, 10)
            if chance <= 3:
                if len(range(max(0, prevLevel-3),  prevLevel)) != 0:
                    nextLevel = random.randint(max(0, prevLevel-3),  prevLevel-1)
                if len(range(prevLevel+1,  prevLevel + 2)) != 0:
                    nextLevel = random.randint(nextLevel, random.randint(prevLevel+1, prevLevel + 2))
            elif chance == 4:
                nextLevel = 0
            else:
                nextLevel = prevLevel
            groundLevel.append(nextLevel)

            isObjectAdded = random.choices([0, 1], [0.7, 0.3])[0]
            if isObjectAdded:
                additionalObjectsList.append(random.choice(additionalObjects))
            else:
                additionalObjectsList.append(0)

            if nextLevel != prevLevel:
                isObjectAdded = random.choices([0, 1], [0.7, 0.3])[0]
                if isObjectAdded:
                    additionalObjectsList.append(random.choice(additionalObjects))
                else:
                    additionalObjectsList.append(0)
                groundLevel.append(nextLevel)
            prevLevel = nextLevel
        print(groundLevel)

    index = 0
    for i in range(0, scrWidth, 64):
        if groundLevel[index] == 0:
            offsetBlit(water1, (i, scrHeight-64))
        elif index != len(groundLevel) -1 and groundLevel[index] > groundLevel[index+1]:
            offsetBlit(ground3, (i, scrHeight-(64*groundLevel[index])))
        elif index != 0 and groundLevel[index] > groundLevel[index-1]:
            offsetBlit(ground1, (i, scrHeight-(64*groundLevel[index])))
        else:
            offsetBlit(ground2, (i, scrHeight-(64*groundLevel[index])))
        for j in range(0, 64*groundLevel[index], 64):
            offsetBlit(ground5, (i, scrHeight-j))
        
        if additionalObjectsList[index] and groundLevel[index]:
            offsetBlit(additionalObjectsList[index], (i, scrHeight-(64*groundLevel[index] + 64)))

        index += 1

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

    if keys[pygame.K_LEFT] and playerMain.x >= playerMain.velocity - 90:
        playerMain.x -= playerMain.velocity
        distance += moveSpeed
        playerMain.left, playerMain.right, playerMain.idle = True, False, False
        playerMain.walkCount += 1
    elif keys[pygame.K_RIGHT] and playerMain.x <= scrWidth - playerMain.width - playerMain.velocity:
        playerMain.x += playerMain.velocity
        distance -= moveSpeed
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


