import pygame
import random
import os

pygame.init()

screenWidth = 600
screenHeight = 400
gap = int(screenHeight/2)
startGravity = 0.1
pygame.display.set_caption("HELICOPTER")

class Actor():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.shape = pygame.Rect(self.x, self. y, self. width, self.height)
        self.graphics = pygame.image.load(os.path.join('actor.gif'))
    def draw(self):
        screen.blit(self.graphics, (self.x, self.y))
    def move(self, v):
        self.y = self.y + v
        self.shape = pygame.Rect(self.x, self. y, self. width, self.height)

class Obstacle():
    def __init__(self, x, obstacleWidth):
        self.x = x
        self.obstacleWidth = obstacleWidth
        self.yUpper = 0
        self.yUpperHeight = random.randint(screenHeight/4, screenHeight/2)
        self.obstacleGap = gap
        #yLower = 100+200=300
        #yLowerHeight = 400-300=100
        self.yLower = self.yUpperHeight + self.obstacleGap
        self.yLowerHeight = screenHeight - self.yLower
        self.color = (0,255,0)
        self.shapeUpper = pygame.Rect(self.x, self.yUpper, self.obstacleWidth, self.yUpperHeight)
        self.shapeLower = pygame.Rect(self.x, self.yLower, self.obstacleWidth, self.yLowerHeight)
    def draw(self):
        pygame.draw.rect(screen, self.color, self.shapeUpper, 0)
        pygame.draw.rect(screen, self.color, self.shapeLower, 0)
    def move(self, v):
        self.x = self.x - v
        self.shapeUpper = pygame.Rect(self.x, self.yUpper, self.obstacleWidth, self.yUpperHeight)
        self.shapeLower = pygame.Rect(self.x, self.yLower, self.obstacleWidth, self.yLowerHeight)
    def crash(self, playerRect):
        if self.shapeUpper.colliderect(playerRect) or self.shapeLower.colliderect(playerRect):
            return True
        else:
            return False
       
screen = pygame.display.set_mode((screenWidth,screenHeight))

def write(text, x, y, size):
    writingFont = pygame.font.SysFont("Arial", size)
    rend = writingFont.render(text, 1, (255, 100, 100))
    screen.blit(rend, (x, y))

def writeInMiddle(text, size):
    writingFont = pygame.font.SysFont("Arial", size)
    rend = writingFont.render(text, 1, (255, 100, 100))
    x = (screenWidth - rend.get_rect().width) /2
    y = (screenHeight - rend.get_rect().height) /2
    screen.blit(rend, (x, y))

activeScreen = "menu"
dy = startGravity
obstacles = []

for i in range (21):
    obstacles.append(Obstacle(i*screenWidth/20, screenWidth/20))

while True:
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = dy - 0.2
            if event.key == pygame.K_DOWN:
                dy = dy + 0.2
            if event.key == pygame.K_SPACE:
                if activeScreen != "play":
                    player = Actor(screenWidth/2, gap/2 + screenHeight/3)
                    dy = startGravity
                    activeScreen = "play"
                    points = 0
                        
    if activeScreen == "menu":#start screen
        write ("HELICOPTER", 20, 20, 50)
        writeInMiddle ("Press space bar to start...", 25)
        logo = pygame.image.load(os.path.join('actor.gif'))
        screen.blit(logo, (400, 40))

    elif activeScreen == "end": #death screen
        write ("HELICOPTER", 20, 20, 50)
        write ("You have crashed! Your score: " + str(points), 20, 100, 25)
        writeInMiddle ("Press space bar to start again...", 25)
        logo = pygame.image.load(os.path.join('actor.gif'))
        screen.blit(logo, (400, 40))

    elif activeScreen == "play":
        for p in obstacles:
            p.move(1)
            p.draw()
            if p.crash(player.shape):
                activeScreen = "end"
        for p in obstacles:
            if p.x <= -p.obstacleWidth:
                obstacles.remove(p)
                obstacles.append(Obstacle(screenWidth, screenWidth/20))
                points = points + 1
        player.draw()
        player.move(dy)
        write ("P: "+str(points), screenWidth - 100, screenHeight - 30, 20)
        
    pygame.display.update()