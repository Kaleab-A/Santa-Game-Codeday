import pygame
import random
import math
import time


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
bulletImage = pygame.image.load(".//Images//bullets//bullet2.png")
bulletImage = pygame.transform.scale(bulletImage, (30, 9))
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

heart = pygame.image.load(".//Images//heart.png")
heart = pygame.transform.scale(heart, (20, 20))

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
        self.health = 100

    def draw(self, win):
        self.x = int(self.x)
        self.y = int(self.y)
        if not self.isJump:
            currentLevelIndex = distance // 64
            if not (currentLevelIndex < 0 or currentLevelIndex > gameLength):
                self.y = int(scrHeight - groundLevel[currentLevelIndex + 9] * 64 - 64 - 50)

        if self.walkCount + 1 > 13*3: self.walkCount = 0
        if self.idle:
            if self.left: win.blit(charL, (self.x - 40, self.y))
            else: win.blit(charR, (self.x, self.y))
        elif self.isJump:
            if self.left: win.blit(charL, (self.x - 40, self.y))
            else: win.blit(charR, (self.x, self.y))
        elif self.left: win.blit(walkLeft[self.walkCount // 3], (self.x - 40, self.y))
        elif self.right: win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
        else: assert 1
        pygame.draw.rect(win, color["red"], (self.x + 40, self.y + 10, self.height, self.width), 1)


class projectile(object):
    def __init__(self, x, y, width, height, color, mousePosition, image):
        self.x = round(x)
        self.y = round(y)
        if type(mousePosition) == tuple:
            self.changeInX = mousePosition[0] -  x
            self.changeInY = -mousePosition[1] + y
        else:
            self.changeInX = mousePosition.x -  x
            self.changeInY = -mousePosition.y + y
        self.width = width
        self.height = height
        self.color = color
        magnitude = math.sqrt(self.changeInX ** 2 + self.changeInY ** 2)
        if magnitude > 0:
            self.changeInX /= magnitude
            self.changeInY /= magnitude
        self.speed = 8
        self.image = image
        
    def draw(self, win, angle):
        win.blit(pygame.transform.rotate(self.image, angle), ((self.x, self.y)))
        pygame.draw.rect(win, color["red"], (self.x, self.y, self.width, self.height), 1)
        # pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    enemyLeft = []
    enemyRight = []
    for i in range(1, 5):
        path = ".//Images//Enemy//Ghost//Png_animation//"
        name = "Ghost" + str(i) + ".png"
        picture = pygame.image.load(path + name)
        # picture = pygame.transform.scale(picture, (186, 128))
        pictureFlip = pygame.transform.flip(picture, True, False)
        enemyLeft.append(picture)
        enemyRight.append(pictureFlip)
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 6
        self.end = 0
        self.walkCount = 0
        self.santaMovment = 0
        self.count = 0
        self.health = 100
        self.target = None
        self.bullets = []
        self.bulletsMove = []
        self.times = 1
        self.bulletSpeed = 40

    def draw(self, win):
        if self.times % 100 == 0:
            bullet = projectile((2*self.x + self.width)//2,  (2*self.y + self.height)//2, 30, 9, color["black"], self.target, bulletImage)
            self.bullets.append(bullet)
            changeX = (self.target.x - bullet.x) 
            changeY = (self.target.y - bullet.y)
            changeX /= self.bulletSpeed
            changeY /= self.bulletSpeed
            self.bulletsMove.append([changeX, changeY])

        self.move()
        # self.y = 300
        # self.y = scrHeight - groundLevel[self.x // 64 + 1] * 64 - 50
        if self.walkCount + 1 >= 4*3:
            self.walkCount = 0
        if self.end >= self.x:
            win.blit(self.enemyRight[self.walkCount // 3], (self.x, self.y))
        else: 
            win.blit(self.enemyLeft[self.walkCount // 3], (self.x, self.y))

        pygame.draw.rect(win, color["red"], (self.x, self.y, self.width, self.height), 1)
        self.times += 1
    
    def move(self):
        # self.x += 1
        # if self.end >= self.x:
        #     self.velocity = abs(self.velocity)
        #     self.walkCount += 1
        # else:
        #     self.velocity = -abs(self.velocity)
        #     self.walkCount +=1
        # ghostMove = random.randint(0, 1)
        # if ghostMove:
        #     self.velocity = abs(self.velocity)
        # else:
        #     self.velocity = -abs(self.velocity)
        # if scrWidth > self.x:
        #     self.velocity = self.velocity
        #     self.walkCount += 1
        #     if scrWidth < 0:
        #         self.velocity = abs(self.velocity)
        # else:
        #     self.velocity = -abs(self.velocity)
        self.walkCount += 1
        # self.x = 400
        # self.x += self.velocity
        # self.santaMovment -= 1

    def hit(self):
        self.count += 1
        self.health -= 50


    def drawBullet(self):
        for bullet in self.bullets:
            # Bullet to Santa Collusion
            currBulletDir = self.bulletsMove[self.bullets.index(bullet)]
            bullet.x += round(currBulletDir[0])
            bullet.y += round(currBulletDir[1])
            if bulletCollid(bullet.x, bullet.y, [self.target]):
                self.bullets.pop(self.bullets.index(bullet))
                self.target.health -= 10
            else:
                angle =  180 - math.degrees( math.atan(currBulletDir[1]/currBulletDir[0]))
                if bullet.x <= self.target.x:
                    angle += 180
                bullet.draw(win, angle)
                
            # Bullet to Love Collusion
            for ghost in ghosts:
                for bullet in ghost.bullets:
                    for santaLove in bullets:
                        if bulletCollid(bullet.x, bullet.y, [santaLove]):
                            ghost.bullets.pop(ghost.bullets.index(bullet))
                            bullets.pop(bullets.index(santaLove))
       
def blitOffset(image, coordinates):
    win.blit(image, (coordinates[0] - distance, coordinates[1]))

playerMain = Player(scrWidth//2, scrHeight-190, 93, 64)
ghosts = []
ghostCount = 10
for i in range(ghostCount):
    ghosts.append(enemy(random.randint(0, scrWidth), random.randint(0, scrHeight-64), 37, 45))
running = True
count = [0]
groundLevel = []
additionalObjectsList = []
gameLength = 100
santaPos = gameLength // 2
bullets = []
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

        for i in range(gameLength):
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

            for i in range(2):
                changeObjectAppear = random.randint(0, 4)
                if changeObjectAppear == 0:
                    changeObject = random.randint(0, 9)
                    additionalObjectsList.append(additionalObjects[changeObject])
                else: additionalObjectsList.append(0)

            groundLevel.append(nextLevel)
            prevLevel = nextLevel

    # drawableGroundLevel = groundLevel[santaPos - (scrWidth//128): santaPos + (scrWidth//128)]
    # drawableObjectList = additionalObjectsList[santaPos - (scrWidth//128): santaPos + (scrWidth//128)]
    index = 0
    for i in range(gameLength):
        i *= 64
        if groundLevel[index] == 0:
            blitOffset(water1, (i, scrHeight-64))
        elif index != len(groundLevel) -1 and groundLevel[index] > groundLevel[index+1]:
            blitOffset(ground3, (i, scrHeight-(64*groundLevel[index])))
        elif index != 0 and groundLevel[index] > groundLevel[index-1]:
            blitOffset(ground1, (i, scrHeight-(64*groundLevel[index])))
        else:
            blitOffset(ground2, (i, scrHeight-(64*groundLevel[index])))
        for j in range(0, 64*groundLevel[index], 64):
            blitOffset(ground5, (i, scrHeight-j))
    
        if additionalObjectsList[index] and groundLevel[index]:
            blitOffset(additionalObjectsList[index], (i, scrHeight-(64*groundLevel[index] + 64)))


        index += 1

def drawHealth(win, pos, healthValue):
    # TODO Conditional Render by using healthValue
    posX = pos[0]
    for i in range(healthValue // 10):
        win.blit(heart, (posX, pos[1]))
        posX += 25

def bulletCollid(bulletX, bulletY, ghosts):
    for ghost in ghosts:
        if type(ghosts) == Player:
            if bulletX > ghost.x + 40 and bulletX < ghost.x + 40 + ghost.width:
                if bulletY > ghost.y and bulletY < ghost.y + ghost.height:
                    return ghost
        else:
            if bulletX > ghost.x and bulletX < ghost.x + ghost.width:
                if bulletY > ghost.y and bulletY < ghost.y + ghost.height:
                    return ghost

    return False
 
def redrawGameWindow():
    for ghost in ghosts:
        if ghost.health <= 0:
            ghosts.pop(ghosts.index(ghost))
    win.blit(bg, (0, 0))
    drawGround()
    playerMain.draw(win)
    drawHealth(win, (700, 30), playerMain.health)
    # ghost1.end = playerMain.x
    for ghost in ghosts:
        ghost.target = playerMain
        ghost.draw(win)
        ghost.drawBullet()
    for bullet in bullets:
        hitGhost = bulletCollid(bullet.x, bullet.y, ghosts)
        if hitGhost:
            bullets.pop(bullets.index(bullet))
            hitGhost.hit()
        else:
            bullet.draw(win, 0)
    count[0] += 1
    pygame.display.update()

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mousePosition = pygame.mouse.get_pos()
            if len(bullets) < 10:
                bullets.append(projectile((2*playerMain.x + playerMain.width)//2,  (2*playerMain.y + playerMain.height)//2, 20, 20, color["red"], mousePosition, heart))

    newBullets = []
    for index in range(len(bullets)):
        bullet = bullets[index]
        if bullet.x  < scrWidth and bullet.x > 0 and bullet.y < scrHeight and bullet.y > 0:
            bullet.x += int(bullet.changeInX * bullet.speed)
            bullet.y -= int(bullet.changeInY * bullet.speed)
            newBullets.append(bullet)  

    bullets = newBullets.copy()      
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and distance > 0:
        # playerMain.x >= playerMain.velocity - 90
        # playerMain.x -= playerMain.velocity
        distance -= moveSpeed
        playerMain.left, playerMain.right, playerMain.idle = True, False, False
        playerMain.walkCount += 1
        santaPos -= 1
        # ghost1.x += 64
        # for ghost in ghosts:
        #     ghost.x += 64
        
    elif keys[pygame.K_RIGHT] and distance < (gameLength - 18) * 64:
        # playerMain.x <= scrWidth - playerMain.width - playerMain.velocity
        # playerMain.x += playerMain.velocity
        distance += moveSpeed
        playerMain.left, playerMain.right, playerMain.idle = False, True, False
        playerMain.walkCount += 1
        santaPos += 1 
        # ghost1.x -= 6
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