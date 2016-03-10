import os, pygame, string, thread, sys, getopt, time, re
from pygame.locals import *
from socket import *
from itertools import chain
from operator import sub

#
#   Globals
#

versionNumber   = 0.01
lineNo          = 0
columnNo        = [0]
serverName      = "localhost"
portNumber      = 7000
programName     = "ptower_NPC"
connectAttempts = 10
wounds          = 0	#Stores the players wounds
fatigue         = 0	#Stores the players fatigue
cRoom           = 0	#Stores the room the player is in
magicArrows     = 0	#Stores the players magic arrows
arrows          = 0	#Stores the players arrows
weight          = 0	#Stores the players total weight
vWall		= []	#Stores the locations of the vertical walls
hWall		= []	#Stores the locations of the horizontal walls
vDoor		= []	#Stores the locations of the vertical doors
hDoor		= []	#Stores the locations of the horizontal doors
treasures	= []	#Stores the locations of the treasures
playerLoc	= []	#Stores the location of the player
prevPlayerLoc	= []	#Stores the previous location of the player
locationChanged	= True
playerDir	= 0	#1 = north, 2 = east, 3 = south, 4 = west
enemies		= []	#Stores the locations of the enemies

def enum(*sequential, **named):	#Custom enum because enums were introduced to python in version 3.4 and I am using 2.7.9
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def connectServer(id, count):
    print "connectServer called"
    global sckt, serverName, portNumber

    sckt = socket(AF_INET, SOCK_STREAM)

    sckt.connect((serverName, portNumber))

def setUpName(): #Bypasses the start screen and then sets the name of the bot to Bot
    global sckt
    print '\nSetting name to Bot. \n'
    time.sleep(0.25)
    sckt.send('\n')
    time.sleep(0.25)
    sckt.send('Bot')
    sckt.send('\n')
    print 'Name has been set and should be in game.\n'


def getWounds(line):
    global wounds
    #
    #Searches the input line for "dW " and then searches the result for an integer and then the global wounds is set the value found
    #
    m = re.search("(dW .*)", line)
    if m:
        #print "search.....", m.group(1)
        tempdW = m.group(1)
        tempdW1 = re.search(r"([0-9]+)", tempdW)
        wounds = tempdW1.group(1)
        #print " Wounds search found ....", wounds

def getRoom(line):
    global cRoom
    #
    #Searches the input line for the room number and sets cRoom to the current room.
    #
    m = re.search("(dR .*)", line)
    if m:
        #print "search.....", m.group(1)
        tempdR = m.group(1)
        tempdR1 = re.search(r"([0-9]+)", tempdR)
        cRoom = tempdR1.group(1)
        #print "Room search found ....", cRoom

def getMArrows(line):
    global magicArrows
    #
    #Searches the input line for the number of magic arrows and sets magicArrows.
    #
    m = re.search("(dM .*)", line)
    if m:
        #print "search.....", m.group(1)
        tempdM = m.group(1)
        tempdM1 = re.search(r"([0-9]+)", tempdM)
        magicArrows = tempdM1.group(1)
        #print "Magic Arrows search found ....", magicArrows

def getArrows(line):
    global arrows
    #
    #Searches the input line for the number of arrows and sets arrows.
    #
    m = re.search("(dA .*)", line)
    if m:
        #print "search.....", m.group(1)
        tempdA = m.group(1)
        tempdA1 = re.search(r"([0-9]+)", tempdA)
        arrows = tempdA1.group(1)
        #print "Arrows search found ....", arrows

def getVWalls(line):
    global vWall
    #
    #Searches the input line for the coordinates of the vWalls and adds them to the vWall list.
    #
    n = re.sub(" +", " ", line)
    m = re.findall("(vwall .*)", n)
    if m:
	#print "search.....", m
	#print "splitting"
	vWall = [i.split()[1:5] for i in m] #lambda loop 
	print "Vertical Walls search found ....", vWall

def getHWalls(line):
    global hWall
    #
    #Searches the input line for the coordinates of the hWalls and adds them to the hWall list.
    #
    n = re.sub(" +", " ", line)
    m = re.findall("(hwall .*)", n)
    if m:
	#print "search.....", m
	#print "splitting"
	hWall = [i.split()[1:5] for i in m]
	print "Horizontal Walls search found ....", hWall

def getVDoor(line):
    global vDoor
    #
    #Searches the input line for the coordinates of the vDoors and adds them to the vDoors list.
    #
    n = re.sub(" +", " ", line)
    m = re.findall("(vdoor .*)", n)
    if m:
	#print "search.....", m
	#print "splitting"
	vDoor = [i.split()[1:5] for i in m]
	print "Vertical Doors search found ....", vDoor

def getHDoor(line):
    global hDoor
    #
    #Searches the input line for the coordinates of the hDoors and adds them to the hDoors list.
    #
    n = re.sub(" +", " ", line)
    m = re.findall("(hdoor .*)", n)
    if m:
	#print "search.....", m
	#print "splitting"
	hDoor = [i.split()[1:5] for i in m]
	print "Horizontal Door search found ....", hDoor

def getTreasure(line):
    global treasures
    #
    #Searches the input line for the coordinates of the treasures and adds them to the treasures list.
    #
    n = re.sub(" +", " ", line)
    m = re.findall("(treasure .*)", n)
    if m:
	#print "splitting"
	treasures = [i.split()[1:3] for i in m]
	print "Treasure search found ....", treasures

def getPlayer(line):
    global playerLoc
    global playerDir
    global prevPlayerLoc
    #
    #Searches the input line for the coordinates of the player and sets the playerLoc list. Then searches for the players facing direction and sets playerDir.
    #
    o = re.sub(" +", " ", line)
    m = re.findall("([swen]man .*)", o)
    if m:
	#print "splitting"
	#print m
	if playerLoc:
	     prevPlayerLoc = playerLoc[0]
	playerLoc[:] = []
	playerDir = 0
	playerLocTemp = [i.split()[1:3] for i in m]
	playerLoc = playerLocTemp[-1]
	#playerLoc[1] = playerLocTemp[-1]
	print "Player found at ....", playerLoc
	#print "Getting direction..."
	#The direction messes up and isn't updated correctly
        n = [i.split()[0] for i in m]
	if n[-1] == "nman":
	    playerDir = 1
	    print "North", playerDir
	elif n[-1] == "eman":
	    playerDir = 2
	    print "East", playerDir
	elif n[-1] == "sman":
	    playerDir = 3
	    print "South", playerDir
	elif n[-1] == "wman":
	    playerDir = 4
	    print "West", playerDir
	#else:
	#    print "Failed to get direction"
	print "prevPlayerLoc ", prevPlayerLoc
	
	#if playerLoc[0] == prevPlayerLoc:
	#    print "Player did not move"
	#else:
	#    print "Player has moved"

def getEnemies(line):
    global enemies
#    global enemiesDir	#For future use to store the enemies direction.
    #
    #Searches the input line for the coordinates of the enemies and adds them to the enemies list.
    #
    n = re.sub(" +", " ", line)
    m = re.findall("([SWEN]man .*)", n)
    if m:
	#print "splitting"
	#print "Before split... ", enemies
	enemies = [i.split()[1:3] for i in m]
	print "Enemy found at ....", enemies

def compareLocations(target):
    global playerLoc
    global prevPlayerLoc
    #
    #Compares the location of the player and that of a target by taking the x and y coords and subtracts them.
    #

    print "Comparing locations"
    tempPlayerLoc = []
    #tempPlayerLoc[0] = playerLoc[-2]
    #tempPlayerLoc[1] = playerLoc[-1]
    tempTarget = list(chain(*target))
    print "tempPlayerLoc = ", tempPlayerLoc
    print "tempTarget = ", tempTarget
    print "playerLoc = ", playerLoc

    playerLocLength = len(playerLoc)
    targetLength = len(tempTarget)
    print "Lengths of playerloc and target....", playerLocLength, targetLength

    if playerLocLength == 2 and targetLength >= 2:
    
	playerLocX = int(playerLoc[-2])
    	playerLocY = int(playerLoc[-1])
    	targetX = int(tempTarget[-2])
    	targetY = int(tempTarget[-1])

    	tempPlayerLoc[:] = []
    	tempTarget[:] = []
    
    	moveX = playerLocX - targetX
    	moveY = playerLocY - targetY

    	print "playerLoc....", playerLocX, playerLocY
    	print "target....", targetX, targetY

    	print "player - target....", moveX, moveY
    	print "Positive x is west.Positive y is north."
    	if moveX > 0:
	    #print "Face west"
	    changeDir(4)
	    time.sleep(0.1)		#Added in time.sleep to stop an issue with the server not handling rapid commands
	    if abs(moveX) != 1:
	        if abs(moveX) > 9:
		    step(9)
	        else:
		    step(abs(moveX))
        elif moveX < 0:
	    #print "Face east"
	    changeDir(2)
	    time.sleep(0.1)
	    if abs(moveX) != 1:
	        if abs(moveX) > 9:
		    step(9)
	        else:
		    step(abs(moveX))
        time.sleep(0.1)
        if moveY > 0:
	    #print "Face north"
	    changeDir(1)
	    time.sleep(0.1)
	    if abs(moveY) != 1:
	        if abs(moveY) > 9:
		    step(9)
	        else:
		    step(abs(moveY))
        elif moveY < 0:
	    #print "Face south"
	    changeDir(3)
	    time.sleep(0.1)
	    if abs(moveY) != 1:
	        if abs(moveY) > 9:
		    step(9)
	        else:
		    step(abs(moveY))

def changeDir(target):
    global playerDir
    #
    #Changes the facing direction based on that of the target direction 1 to 4
    #
    print "Player direction ", playerDir
    print "Target direction ", target
    absChange = abs(target - playerDir)
    change = (target - playerDir)
    print "Change....", change
    if absChange == 2:
	#print "U-turn"
	vault()
	playerDir = target

    elif playerDir == 4 and target == 1:
	turnRight()
	playerDir = target
    elif playerDir == 1 and target == 4:
	turnLeft()
	playerDir = target
    elif change > 0:
	if absChange == 3:
	    turnLeft()
	    playerDir = target
	else:
	    turnRight()
	    playerDir = target
    elif change < 0:
	if absChange == 3:
	    turnRight()
	    playerDir = target
	else:
	    turnLeft()
	    playerDir = target
    else:
	print "Direction not changed!"
    time.sleep(0.1)

def processLine(line):
    getWounds(line)
    getRoom(line)
    getMArrows(line)
    getArrows(line)
    getVWalls(line)
    getHWalls(line)
    getVDoor(line)
    getHDoor(line)
    getTreasure(line)
    getPlayer(line)
    getEnemies(line)

def step(steps):
    global sckt
    strSteps = str(steps)
    sckt.send(strSteps)
    print 'Stepping forward ', strSteps

def step1():
    global sckt
    sckt.send('1')
    print 'Stepping forward 1'

def step2():
    global sckt
    sckt.send('2')
    print 'Stepping forward 2'

def step3():
    global sckt
    sckt.send('3')
    print 'Stepping forward 3'

def step4():
    global sckt
    sckt.send('4')
    print 'Stepping forward 4'

def step5():
    global sckt
    sckt.send('5')
    print 'Stepping forward 5'

def step6():
    global sckt
    sckt.send('6')
    print 'Stepping forward 6'
    
def turnLeft():
    global sckt
    sckt.send('l')
    print 'Turning left'

def turnRight():
    global sckt
    sckt.send('r')
    print 'Turn right'

def vault():
    global sckt
    sckt.send('v')
    print 'Vaulting'
    
def attack():
    global sckt
    sckt.send('a')
    print 'Attacking'

def openDoor():
    global sckt
    sckt.send('o')
    print 'Opening door'

def fireNArrow():
    global sckt
    sckt.send('f')
    print 'Firing a normal arrow'

def fireMArrow():
    global sckt
    sckt.send('m')
    print 'Firing a magic arrow'

def parry():
    global sckt
    sckt.send('p')
    print 'Parrying'

def thrust():
    global sckt
    sckt.send('t')
    print 'Thrusting'

def closeDoor():
    global sckt
    sckt.send('c')
    print 'Closing door'

def examineDoor():
    global sckt
    sckt.send('e')
    print 'Examining door'

def pickUpTreasure():
    global sckt
    sckt.send('g')
    print 'Getting treasure'

def dropTreasure():
    global sckt
    sckt.send('d')
    print 'Dropping treasure'

def useTreasure():
    global sckt
    sckt.send('u')
    print 'Using treasure'

def speak():
    global sckt
    sckt.send('s')
    print 'Speaking'

def stripclrf(s):
    return s[:-1]
    
def initEventLoop():
    print "initEventLoop called"
    global sckt

    #thread.start_new(connectServer, (1,connectAttempts))

    targetEnum	= enum('TREASURE', 'ENEMIES', 'HDOOR', 'VDOOR')
    connectServer(1, connectAttempts)
    setUpName()

    f = sckt.makefile("rb")
    line = stripclrf(f.readline())
    
    time.sleep(1)

    while True:
        line = sckt.recv(1024)
        processLine(line)
        time.sleep(0.1)
	if locationChanged:	    
	    if treasures:
		compareLocations(treasures)
	    	print "Treasures...", treasures
		treasures[:] = []
	    elif enemies:
		compareLocations(enemies)
		print "Enemies...", enemies
		enemies[:] = []
	    elif vDoor:
		compareLocations(hDoor)
		print "hDoors...", hDoor
		hDoor[:] = []
	    elif vDoor:
		compareLocation(vDoor)
		print "vDoors...", vDoor
		vDoor[:] = []
	    else:
	    	print "Nothing found."
	time.sleep(0.1)

def initNPC():
    print "initNPC called"
    initEventLoop()
    
def main():
    print "main called"
    initNPC()

if __name__ == '__main__': main()
