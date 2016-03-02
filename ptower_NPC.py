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
wounds          = 10
fatigue         = 100
cRoom           = 0
magicArrows     = 0
arrows          = 0
weight          = 0
vWall		= [0]
hWall		= [0]
vDoor		= [0]
hDoor		= [0]
treasures	= [0]
playerLoc	= [0]
playerDir	= 0	#1 = north, 2 = east, 3 = south, 4 = west
enemies		= [0]


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
        print " Wounds search found ....", wounds

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
        print "Room search found ....", cRoom

def getMArrows(line):
    global magicArrows

    m = re.search("(dM .*)", line)
    if m:
        #print "search.....", m.group(1)
        tempdM = m.group(1)
        tempdM1 = re.search(r"([0-9]+)", tempdM)
        magicArrows = tempdM1.group(1)
        print "Magic Arrows search found ....", magicArrows

def getArrows(line):
    global arrows

    m = re.search("(dA .*)", line)
    if m:
        #print "search.....", m.group(1)
        tempdA = m.group(1)
        tempdA1 = re.search(r"([0-9]+)", tempdA)
        arrows = tempdA1.group(1)
        print "Arrows search found ....", arrows

def getVWalls(line):
    global vWall

    m = re.findall("(vwall .*)", line)
    if m:
	#print "search.....", m
	print "splitting"
	vWall = [i.split()[1:5] for i in m] #lambda loop 
	print "Vertical Walls search found ....", vWall

def getHWalls(line):
    global hWall

    m = re.findall("(hwall .*)", line)
    if m:
	#print "search.....", m
	print "splitting"
	hWall = [i.split()[1:5] for i in m]
	print "Horizontal Walls search found ....", hWall

def getVDoor(line):
    global vDoor

    m = re.findall("(vdoor .*)", line)
    if m:
	#print "search.....", m
	print "splitting"
	vDoor = [i.split()[1:5] for i in m]
	print "Vertical Doors search found ....", vDoor

def getHDoor(line):
    global hDoor

    m = re.findall("(hdoor .*)", line)
    if m:
	#print "search.....", m
	print "splitting"
	hDoor = [i.split()[1:5] for i in m]
	print "Horizontal Door search found ....", hDoor

def getTreasure(line):
    global treasures

    m = re.findall("(treasure .*)", line)
    if m:
	print "splitting"
	treasures = [i.split()[1:3] for i in m]
	print "Treasure search found ....", treasures

def getPlayer(line):
    global playerLoc
    global playerDir

    m = re.findall("([swen]man .*)", line)
    if m:
	print "splitting"
	playerLoc = [i.split()[1:5] for i in m]
	print "Player found at ....", playerLoc
	print "Getting direction..."
        n = [i.split()[0] for i in m]
	if n[0] == "nman":
	    playerDir = 1
	    print "North", playerDir
	elif n[0] == "eman":
	    playerDir = 2
	    print "East", playerDir
	elif n[0] == "sman":
	    playerDir = 3
	    print "South", playerDir
	elif n[0] == "wman":
	    playerDir = 4
	    print "West", playerDir
	else:
	    print "Failed to get direction"

def getEnemies(line):
    global enemies
#    global enemiesDir

    m = re.findall("([SWEN]man .*)", line)
    if m:
	print "splitting"
	enemies = [i.split()[1:5] for i in m]
	print "Enemy found at ....", enemies

def compareLocations(target):
    global playerLoc
    print "Comparing locations"
    tempPlayerLoc = list(chain(*playerLoc))
    tempTarget = list(chain(*target))
    print tempPlayerLoc
    
    playerLocX = int(tempPlayerLoc[0])
    playerLocY = int(tempPlayerLoc[1])
    targetX = int(tempTarget[0])
    targetY = int(tempTarget[1])
    
    print targetX, targetY
    moveX = playerLocX - targetX
    moveY = playerLocY - targetY

    print "player x - target x....", moveX, moveY

    

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
    global sckt, wounds

    #thread.start_new(connectServer, (1,connectAttempts))

    connectServer(1, connectAttempts)
    setUpName()

    f = sckt.makefile("rb")
    line = stripclrf(f.readline())
    
    while True:
        line = sckt.recv(1024)
        print "Processing line", line, "\n"
        processLine(line)
        time.sleep(0.1)
        print "Wounds: ", wounds
        if int(playerDir) == 1:  
            print "I am facing North"
	    turnLeft()
            step2()
	else:
	    turnRight()
	if treasures:
	    compareLocations(treasures)
	time.sleep(5)
#        step1()
#        time.sleep(1)
#        turnLeft()
#        time.sleep(1)
#        turnRight()
#        time.sleep(1)
#        attack()

def initNPC():
    print "initNPC called"
    initEventLoop()
    
def main():
    print "main called"
    initNPC()

if __name__ == '__main__': main()
