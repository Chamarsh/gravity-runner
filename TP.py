from cmu_112_graphics import *
from PIL import ImageEnhance
import random
'''
Project: Gravity Style Jetpack Joyride style game
Main Components:
Background: create a moving background which can potentially change
as the player progress throughout the game
Platforms: create platforms which the player can step on but if player misses
and exits the screen then they will lose the game, the platforms can come 
in a few different forms with some having unique designs
Gravity: create a realistic form of gravity that can be changed at every
click of the space bar
Enemies: must create enemies throughout the game which can take lives away
from the player if the enemy makes contact with it, there can only be 
one enemy at a time on the screen
Powerups: Be able to place powerups on the screen which if will be activated
only if the player makes contact with it, space the powerups out so they 
are not continous but more like random throughout the game

'''
#class for platforms
class platform(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x1 = self.x + 384
        self.y1 = self.y + 75

    def location(self):
        return (self.x, self.y, self.x1, self.y1)

    def changeLocation(self, distance):
        self.x -= distance
        self.x1 -= distance


#class for walls
class wall(object):
    def __init__(self, x, y, x1, y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
    
    def location(self):
        return (self.x, self.y, self.x1, self.y1)

    def changeLocation(self, distance):
        self.x -= distance
        
        self.x1 -= distance
        
#class for blocks
class block(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x1 = x + 75
        self.y1 = y + 75

    def location(self):
        return (self.x, self.y, self.x1, self.y1)

    def changeLocation(self, distance):
        self.x -= distance
        
        self.x1 -= distance
        
#class for the character
class character(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x1 = x + 50
        self.y1 = y + 50

    def location(self):
        return self.x, self.y, self.x1, self.y1

    def moveForward(self, distance):
        self.x += distance
        self.x1 += distance

    def changeGravity(self, distance):
        self.y -= distance
        self.y1 -= distance

    def hitWall(self, distance):
        self.x -= distance
        self.x1 -= distance

#class for powerups
class powerup(object):
    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y
        self.x1 = x + 50
        self.y1 = y + 50
        self.c = 'yellow'
        if num == 1:
            self.c = 'red'
        elif num == 2:
            self.c = 'blue'
        elif num == 3:
            self.c = 'white'
        

    def location(self):
        return self.x, self.y, self.x1, self.y1

    def changeLocation(self, distance):
        self.x -= distance
        self.x1 -= distance

    def color(self):
        return self.c

#class for the path
class path(object):
    def __init__(self, x, y, x1, y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1

    def location(self):
        return self.x, self.y, self.x1, self.y1

    def changeLocation(self, distance):
        self.x -= distance
        self.x1 -= distance

#app started function containing essential global variables
def appStarted(app):
    app.background = app.loadImage('background0.gif')
    app.title = app.loadImage('title.gif')
    app.gameOverTitle = app.loadImage('gameover.gif')
    app.startingScreen = True
    app.platforms = []
    app.objects = []
    app.timerDelay = 1
    app.powerups = []
    app.numPowerups = 0
    app.timer = 0
    app.path = []
    app.platformLength = app.width/5
    app.score = 0
    app.speed = 15
    app.pushback = 0
    app.characterSpeed = 15
    app.gravity = 'down'
    app.character = character(app.width/5, app.height/2)
    app.gameOver = False
    startingPlatforms(app)
    startingPath(app)
    if app.startingScreen == False:
        appStartedHelper(app)

#Allows you to restart game without returning to homescreen
def appStartedHelper(app):
    app.platforms = []
    app.blocks = []
    app.score = 0


#creates the starting platforms
def startingPlatforms(app):
    if len(app.platforms) == 0:
        for i in range(6):
            pT = platform(app.width/5*i , 0)
            pB = platform(app.width/5*i, app.height-75)
            app.platforms.append((pT,pB))

#creates the starting path
def startingPath(app):
    for i in range(6):
        p = path(app.width/5*i, app.height/2, app.width/5*i + app.width/5, app.height/2)
        app.path.append(p)

#This function creates the enemies along with their location on screen
def enemy(app):
    pass





#Draws the character that will be played by the player
def drawCharacter(app, canvas):
    (x, y, x1, y1) = app.character.location()
    canvas.create_rectangle(x, y, x1, y1, fill = 'orange')



#function that moves the platforms on the screen
def movePlatforms(app):
    for platform in app.platforms:
        (top, bottom) = platform
        top.changeLocation(app.speed)
        bottom.changeLocation(app.speed)
    for object in app.objects:
        object.changeLocation(app.speed)
    for powerup in app.powerups:
        powerup.changeLocation(app.speed)

#changes the gravity of the character
def moveCharacter(app):
    if app.gravity == 'down':
        app.character.changeGravity(-1 * app.characterSpeed)
    else:
        app.character.changeGravity(app.characterSpeed)

#moves the solved path along the screen
def movePath(app):
    for p in app.path:
        p.changeLocation(app.speed)

#checks if the character has hit a platform
def checkHitPlatform(app):
    for object in app.objects:
        x, y, x1, y1 = object.location()
        cx, cy, cx1, cy1 = app.character.location()
        y<=cy<= y1 and x<=cx<=x1 or y<=cy1<= y1 and x<=cx1<=x1
    for platform in app.platforms:
        top, bottom = platform
        tx, ty, tx1, ty1 = top.location()
        bx, by, bx1, by1 = bottom.location()
        cx, cy, cx1, cy1 = app.character.location()
        if ty<=cy<= ty1 and tx<=cx<=tx1 or ty<=cy1<= ty1 and tx<=cx1<=tx1\
         or by<=cy<=by1 and bx<=cx<=bx1 or by<=cy1<=by1 and bx<=cx1<=bx1:
            return True
    return False

#doesnt let character go past platform if he collides with it
def hitPlatform(app):
    if checkHitPlatform(app):
        if app.gravity == 'up':
            app.character.changeGravity(-1 * app.characterSpeed)
        else:
            app.character.changeGravity(app.characterSpeed)

#checks to see if the character collides with an object
def hitWall(app):
    for platform in app.platforms:
        top, bottom = platform
        tx, ty, tx1, ty1 = top.location()
        bx, by, bx1, by1 = bottom.location()
        cx, cy, cx1, cy1 = app.character.location()
        if ((ty<=cy<=ty1 or ty<=cy1<ty1) and tx<=cx1<=tx1) or\
         ((by<=cy<=by1 or by<=cy1<by1) and bx<=cx1<=bx1):
            return True
    for object in app.objects:
        x, y, x1, y1 = object.location()
        cx, cy, cx1, cy1 = app.character.location()
        if (y<=cy<=y1 or y <=cy1<=y1) and x<=cx1<=x1:
            return True
    return False

#randomly generates objects on the path
def generateObjects(app):
    num = random.randint(0, 2)
    newT = platform(app.width, 0 + 75*num)
    newB = platform(app.width, app.height - 75*num)
    res = random.randint(1, 3)
    app.platforms.append((newT, newB))
    if res == 1:
        temp =  random.randint(1, 3)
        if temp == 1:
            loc = random.randint(1,3)
            b = block(app.width, app.height - 75*(2 + loc))
            app.objects.append(b)
        else:
            w = wall(app.width, app.height - 75*(3+temp), app.width+75,\
            app.height - 75*(3 + num))
            app.objects.append(w)
        

#finds space to place down powerups and objects
def findSpace(app):
    if len(app.platforms) == 0:
        return None
    if len(app.objects) == 0:
        return None
    top, bottom = app.platforms[len(app.platforms)-1]
    tx, ty, tx1,ty1 = top.location()
    bx, by, bx1, by1 = bottom.location()
    #object = app.objects[len(app.objects)-1]
    #ox, oy, ox1, oy1 = object.location()
    for loc in range(int((by + ty1)/2), ty1, -1):
        if loc + 50 <= by :
            return loc
    return None  

#activates the powerups     
def usePowerup(app, i):
    pu = app.powerups[i]
    ability = pu.color()
    app.powerups.pop(i)
    if ability == 'yellow':
        app.score += 100
    elif ability == 'red':
        pass
    elif ability == 'blue':
        pass
    elif ability == 'white':
        pass

#checks to see if the player has gotten a powerup
def getPowerup(app):
    i = 0
    for power in app.powerups:
        px, py, px1, py1 = power.location()
        x, y, x1, y1 = app.character.location()
        if px<=x1<=px1 and py<=y1<=py1 or px<=x1<=px1 and py<=y<=py1 or\
            px<=x<=px1 and py<=y1<=py1 or px<=x<=px1 and py<=y<=py1:
                ability = power.color()
                app.powerups.pop(i)
                if ability == 'yellow':
                    app.score += 100
                elif ability == 'red':
                    pass
                elif ability == 'blue':
                    pass
                elif ability == 'white':
                    pass
        else:
            i += 1

#randomly generates powerups on the path
def generatePowerUp(app):
    if app.numPowerups % 2 == 1:
        num = random.randint(1, 20)
        res = None
        if num in range(1, 10):
            res = findSpace(app)
        if res != None:
            a = powerup(num, app.width, res)
            app.powerups.append(a)

#Draws the platforms on the top and bottom of the screen
#platforms can be at very bottom or can be towards the middle
#There can also be more than 1 set of platforms creating pathways for player
#to go through
def drawPlatforms(app, canvas):
    for object in app.objects:
        x, y, x1, y1 = object.location()
        canvas.create_rectangle(x, y, x1, y1, fill = 'gray', width = 5)
    for platform in app.platforms:
        top, bottom = platform
        tX, tY, tX1, tY1 = top.location()
        bX, bY, bX1, bY1 = bottom.location()
        canvas.create_rectangle(tX, tY, tX1, tY1, fill = 'gray', width = 5)
        canvas.create_rectangle(bX, bY, bX1, bY1, fill = 'gray', width = 5)
    for powerups in app.powerups:
        color = powerups.color()
        x, y, x1, y1 = powerups.location()
        canvas.create_oval(x, y, x1, y1, fill = color)

#checks if the player has lost
def checkGameOver(app):
    x, y, x1, y1 = app.character.location()
    if x1 <= 0 or y1 <= 0 or y >= app.height:
        app.gameOver = True

#verifies that the new coordinate for the path is valid
def pathIsValid(app, x, y, x1, y1):
    for platform in app.platforms:
        top, bottom = platform
        tx, ty, tx1, ty1, = top.location()
        bx, by, bx1, by1 = bottom.location()
        if ty<=y1<=ty1 or by<=y1<=by1:
            return False
    for object in app.objects:
        ox, oy, ox1, oy1 = object.location()
        if oy<=y1<=oy1:
            return False
    return True

#finds the best path for the player
def pathSolver(app):
    pat = app.path[len(app.path)-1]
    x, y, x1, y1 = pat.location()
    a, b, a1, b1 = pathSolverHelper(app, x1, y1, x1 + 15, y1)
    p = path(a, b, a1, b1)
    app.path.append(p)

#helper function to finding the best path
def pathSolverHelper(app, x, y, x1, y1):
    if pathIsValid(app, x, y, x1, y1):
        return x, y, x1, y1
    else:
        for i in range(300):
            a = path(x, y, x1, y1)
            app.path.append(a)
            solution = pathSolverHelper(app, x, y, x1, y1 - 150 + i)
            if solution != None:
                return solution
            app.path.pop()
        return None

#draws the path on the screen
def drawPath(app, canvas):
    for p in app.path:
        x, y, x1, y1 = p.location()
        canvas.create_line(x, y, x1, y1, fill = 'green', width = 3)

#will indicate speed at which player will progress
#the longer the player survives the faster the game will get
def timerFired(app):
    app.timerDelay = 1
    if app.timer % 10 == 0:
        app.score += 1
    if app.gameOver or app.startingScreen:
        return
    app.timer += 1
    if app.timer % 10 == 0:
        if app.pushback > 0:
            app.character.moveForward(50)
            app.pushback -= 1
    if app.score % 50 == 0:
        app.speed += 1
    movePlatforms(app)
    movePath(app)
    if hitWall(app):
        app.character.hitWall(50)
        app.pushback += 1
    moveCharacter(app)
    hitPlatform(app)
    (top, bottom) = app.platforms[0]
    (x, y, x1, y1) = top.location()
    if x1 <= 0:
        app.platforms.pop(0)
        app.numPowerups += 1
        generateObjects(app)
        generatePowerUp(app)
    pathSolver(app)
    getPowerup(app)
    checkGameOver(app)
    
    

#This function will mainly be used for main screen and game over situations
def mousePressed(app, event):
    if app.startingScreen:
        if event.x and event.y:
            app.startingScreen = False
    if app.gameOver == True:
        if event.x and event.y:
            app.startingScreen = True
            app.gameOver == False
            appStarted(app)
    

#allows the player to change gravity using the spacebar
def keyPressed(app, event):
    if event.key == 'Space':
        if app.gravity == 'down':
            app.gravity = 'up'
        else:
            app.gravity = 'down'

#This function will draw the game over screen in the case in which the 
#player has lost
def drawGameOver(app, canvas):
    pass


def drawScore(app, canvas):
    canvas.create_text(app.width/2, app.height/10, text = 'Score = ' + str(app.score), font = 'Arial 20')

def startingScreen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))
    canvas.create_image(app.width/2, app.height/5, image=ImageTk.PhotoImage(app.title))
    canvas.create_text(app.width/2, app.height/2, text = 'Click anywhere to begin!', font = 'Arial 30')
    canvas.create_text(app.width/2, app.height/1.5, text = 'Remember: use the space bar to avoid the objects and survive as long as you can', fill = 'red', font = 'Arial 15')
    canvas.create_text(app.width/2, app.height/1.5+25, text = 'collecting coins will increase your score'\
    ,fill = 'red', font = 'Arial 15')
    canvas.create_text(app.width/2, app.height/1.5+50, text = 'GOOD LUCK!', fill = 'red', font = 'Arial 15')

def startGame(app, canvas):
    if app.gameOver == True:
        drawGameOver(app, canvas)
        canvas.create_image(app.width/2, app.height/5, image=ImageTk.PhotoImage(app.gameOverTitle))
        canvas.create_text(app.width/2, app.height/2, text = 'Nice Try you had a score of ' + str(app.score), fill = 'red',font = 'Arial 30')
        canvas.create_text(app.width/2, app.height/2+45, text = 'Click anywhere to return to the main menu!', fill = 'red', font = 'Arial 30')
        
    else:
        drawPlatforms(app, canvas)
        drawCharacter(app, canvas)
        drawPath(app, canvas)
        drawScore(app, canvas)




#This function will draw all the components in the necessary space
def redrawAll(app, canvas):
    if app.startingScreen:
        startingScreen(app, canvas)
    else:
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))

        startGame(app, canvas)


runApp(width=1200, height=500)