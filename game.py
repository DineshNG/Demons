import pygame
import random

# initialize pygame
pygame.init()

# set window dimensions
windowwidth, windowheight = 799, 532

# display window and title
win = pygame.display.set_mode((windowwidth, windowheight))
pygame.display.set_caption("DEMONS")

# load sprites and sounds
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
char = pygame.image.load('standing.png')
bg = pygame.image.load('bg.jpg')
bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
# score variable
score = 0
start_ticks = 0
end_ticks = 0
# game clock
clock = pygame.time.Clock()


# player class
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = True
        self.walkCount = 0
        # self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 28, 54)
        self.health = 50

    def draw(self, win):
        if man.health:
            if not (self.standing):
                if self.walkCount + 1 >= 27:
                    self.walkCount = 0
                if self.left:
                    win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.left:
                    win.blit(walkLeft[0], (self.x, self.y))
                else:
                    win.blit(walkRight[0], (self.x, self.y))
            self.hitbox = (self.x + 17, self.y + 11, 28, 54)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0] - 5, self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 240, 0), (self.hitbox[0] - 5, self.hitbox[1] - 20, self.health, 10))
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 20
        self.y = windowheight-30-self.height
        self.right = True
        self.left = False
        self.walkCount = 0
        self.health -= 10
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (windowwidth // 2 - (text.get_width() / 2), windowheight // 2))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


# projectile class
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing

    def draw(self, win):
        # pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        if man.right and not man.left:
            pygame.draw.polygon(win, self.color,
                                [(self.x + 20, self.y + 5), (self.x + 20, self.y - 5), (self.x + 25, self.y)])
            pygame.draw.line(win, self.color, (self.x, self.y), (self.x + 20, self.y))
            pygame.draw.polygon(win, self.color, [(self.x - 5, self.y + 5), (self.x - 5, self.y - 5), (self.x, self.y)])
        elif man.left and not man.right:
            pygame.draw.polygon(win, self.color,
                                [(self.x - 20, self.y + 5), (self.x - 20, self.y - 5), (self.x - 25, self.y)])
            pygame.draw.line(win, self.color, (self.x, self.y), (self.x - 20, self.y))
            pygame.draw.polygon(win, self.color, [(self.x + 5, self.y + 5), (self.x + 5, self.y - 5), (self.x, self.y)])


# enemy class
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end, bossLevel=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [20+man.width, self.end]  #################################################################################
        self.walkCount = 0
        self.bossLevel = bossLevel
        self.vel = 3 * self.bossLevel
        self.hitbox = (self.x + 15, self.y + 2, 32, 57)
        self.health = 10 * self.bossLevel
        self.visible = True


    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 15, self.y + 2, 32, 57)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0] - 5, self.hitbox[1] - 20, 50 , 10))
            pygame.draw.rect(win, (0, 240, 0), (self.hitbox[0] - 5, self.hitbox[1] - 20, round(5 * self.health / self.bossLevel),10))
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
                if self.y + self.height + 20 < windowheight:
                    self.y += self.vel//random.randint(1,10)
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
                if self.y > windowheight//2:
                    self.y += self.vel//random.randint(1,10)
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
            global start_ticks
            start_ticks = pygame.time.get_ticks()
        print(f'Score: {score}')

    def respawn(self):
        if self.visible == False:
            global end_ticks
            end_ticks = pygame.time.get_ticks()
            if end_ticks - start_ticks >= 3000:
                global goblin
                goblin = enemy(windowwidth +20, windowheight-30-self.height, 64, 64, windowwidth-self.width-20, goblin.bossLevel+1)
                self.visible = True




# redraw window function
def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (10, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.draw.rect(win, (6, 125, 8), (0, windowheight-30 , windowwidth, 30))
    if goblin.visible == False and goblin.bossLevel<6:
        text2 = font.render('RESPAWNING...', 1, (0, 0, 0))
        win.blit(text2, (windowwidth // 2 - (text2.get_width() / 2), windowheight // 2))
    if man.health <= 0:
        gameover = font.render('GAME OVER! Press R to Restart', 1, (0,0,0))
        win.blit(gameover, (windowwidth // 2 - (gameover.get_width() / 2), windowheight // 2))
    if goblin.bossLevel == 7:
        winmsg = font.render('YOU WIN, Exiting in 3s', 1, (0, 0, 0))
        win.blit(winmsg, (windowwidth // 2 - (winmsg.get_width() / 2), windowheight // 2))

    pygame.display.update()


# mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(20, windowheight-30-64, 64, 64)  # create player instance
goblin = enemy(250, windowheight-30-64, 64, 64, windowwidth-20-64)  # create enemy instance
shootLoop = 0  # for separate bullets
bullets = []  # no of bullets list

run = True
while run:
    clock.tick(27)  # set framerate
    if goblin.bossLevel == 7:
        pygame.time.delay(3000)
        break
    if goblin.visible == True and man.health:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for bullet in bullets:
        if goblin.visible == True and man.health:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > \
                    goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                        goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < windowwidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            try:
                bullets.pop(bullets.index(bullet))
            except ValueError:
                pass

    keys = pygame.key.get_pressed()
    if man.health:
        if keys[pygame.K_SPACE] and shootLoop == 0:
            bulletSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                bullets.append(
                    projectile(round(man.x + (man.width) // 2), round(man.y + (man.height) // 2), 6, (255, 225, 0), facing))
            shootLoop = 1

        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < windowwidth - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0
        if not (man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                # man.right = False
                # man.left = False
                # man.standing = True
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10

    if goblin.visible == False:
        goblin.respawn()

    if man.health <= 0:
        if keys[pygame.K_r]:
            man.health = 50


    for event in pygame.event.get():  # gets a list
        if event.type == pygame.QUIT:
            run = False
    redrawGameWindow()

pygame.quit()
