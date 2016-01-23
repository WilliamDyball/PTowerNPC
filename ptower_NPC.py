import os, pygame, string, thread, sys, getopt, time
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


def connectServer(id, count):
    print "connectServer called"
    global sckt, serverName, portNumber

    # s = open('testscript', 'r')
    # line = s.readline()
    while True:
        sckt = socket(AF_INET, SOCK_STREAM)
        print "attempting to connect to %s:%d" % (serverName, portNumber)
        try:
            sckt.connect((serverName, portNumber))
            break
        except error, why:
            print "cannot find server on %s:%d" % (serverName, portNumber)
            count -= 1
            if count>0:
                print "will try again"
                portNumber += 1
            else:
                print "cannot connect to %s:%d the server is probably not running or it is not accessible" % (serverName, portNumber)
                sys.exit(0)
        
    #f = sckt.makefile("rb")
    #line = stripcrlf(f.readline())
    #while line:
        #print line
        # line = s.readline()
        #line = stripcrlf(f.readline())
        #print "line =", line, " thus stopping"

def setUpName(): #Bypasses the start screen and then sets the name of the bot to Bot
    global sckt
    print('\nSetting name to Bot. \n')
    time.sleep(0.25)
    sckt.send('\n')
    time.sleep(0.25)
    sckt.send('Bot')
    sckt.send('\n')
    print('Name has been set and should be in game.\n')
        
def step1():
    global sckt
    sckt.send('1')
    print('Stepping forward 1')

def setp2():
    global sckt
    sckt.send('2')
    print('Stepping forward 2')
    
def turnLeft():
    global sckt
    sckt.send('l')
    print('Turning left')

def turnRight():
    global sckt
    sckt.send('r')
    print('Turn right')

def vault():
    global sckt
    sckt.send('v')
    print('Vaulting')
    
def attack():
    global sckt
    sckt.send('a')
    print('Attacking')

def openDoor():
    global sckt
    sckt.send('o')
    print('Opening door')

def fireNArrow():
    global sckt
    sckt.send('f')
    print('Firing a normal arrow')

def fireMArrow():
    global sckt
    sckt.send('m')
    print('Firing a magic arrow')

def parry():
    global sckt
    sckt.send('p')
    print('Parrying')

def thrust():
    global sckt
    sckt.send('t')
    print('Thrusting')

def closeDoor():
    global sckt
    sckt.send('c')
    print('Closing door')

def examineDoor():
    global sckt
    sckt.send('e')
    print('Examining door')

def getTreasure():
    global sckt
    sckt.send('g')
    print('Getting treasure')

def dropTreasure():
    global sckt
    sckt.send('d')
    print('Dropping treasure')

def useTreasure():
    global sckt
    sckt.send('u')
    print('Using treasure')

def speak():
    global sckt
    sckt.send('s')
    print('Speaking')
    
def initEventLoop():
    print "initEventLoop called"
    global sckt

    thread.start_new(connectServer, (1,connectAttempts))

    setUpName()
    
    while True:
        time.sleep(1)
        step1()
        time.sleep(1)
        turnLeft()
        time.sleep(1)
        turnRight()
        time.sleep(1)
        attack()

def initNPC():
    print "initNPC called"
    initEventLoop()
    
def main():
    print "main called"
    initNPC()

if __name__ == '__main__': main()
