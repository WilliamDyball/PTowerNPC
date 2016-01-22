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
    

def initEventLoop():
    print "initEventLoop called"
    global sckt

    thread.start_new(connectServer, (1,connectAttempts))

    # Skips the start screen and sets the name to Bot.
    time.sleep(1)
    sckt.send('\n')
    time.sleep(1)
    sckt.send('Bot')
    sckt.send('\n')

    print "Should be in game"
    while True:
        time.sleep(2)
        sckt.send('1')
        time.sleep(2)
        sckt.send('l')
        time.sleep(2)
        sckt.send('r')

def initNPC():
    print "initNPC called"
    initEventLoop()
    
def main():
    print "main called"
    initNPC()

if __name__ == '__main__': main()
