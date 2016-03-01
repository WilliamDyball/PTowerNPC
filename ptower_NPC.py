import os, pygame, string, thread, sys, getopt, time, re
from pygame.locals import *
from socket import *

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
players		= [0]
playerDir	= [0]


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
	vWall = [i.split()[1:5] for i in m]
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

def getPlayers(line):
    global players

    m = re.findall("(man .*)", line)
    if m:
	print "splitting"
	players = [i.split()[1:5] for i in m]
	print "Players found at ....", players

def processLine(line):
    getWounds(line)
    getRoom(line)
    getMArrows(line)
    getArrows(line)
    getVWalls(line)
    getHWalls(line)
    getVDoor(line)
    getHDoor(line)
    getPlayers(line)
    
def step1():
    global sckt
    sckt.send('1')
    print 'Stepping forward 1'

def step2():
    global sckt
    sckt.send('2')
    print 'Stepping forward 2'
    
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

def getTreasure():
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
        if int(wounds) <= 75:  #Sets wounds to be an int to be evaluated
            print "low health"
            vault()
            step2()
        step1()
        time.sleep(1)
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
