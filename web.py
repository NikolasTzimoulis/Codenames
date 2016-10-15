# -*- coding: utf-8 -*- 
from bottle import route, run, request, template, static_file
import random 

wordFile = 'words-el.txt'
newgameHtml = ""
deckSize=25
wordList = []
for word in open(wordFile, 'r'):
    wordList.append(word)
playerDict = {}
gameOver = False
teams = {'blue':[], 'red':[]}
spymasters = []
wordsSample = []
spies = []
revealed = []
    
def getTeam(ip):
    for teamname in teams.keys():
        if ip in teams[teamname]:
            return teamname
        
def getPlayerClass(ip):
    playerClass = ""
    playerClass += getTeam(ip)+"player"
    if ip in spymasters:
        playerClass += " spymaster"
    return playerClass    

def setupMatch():
    global wordsSample, blue_first, spymasters, spies, revealed, gameOver
    gameOver = False
    spymasters = []
    wordsSample = random.sample(wordList, deckSize)
    revealed = [False] * deckSize
    r = b = 8
    blue_first = (random.randint(0,1) == 0)
    if blue_first: b += 1 
    else: r += 1
    spies = [0]*deckSize
    spies[random.randint(0,deckSize-1)] = -1 
    while b > 0 or r > 0:
        pos = random.randint(0,deckSize-1)
        if spies[pos] == 0:
            if b > 0:
                spies[pos] = 1
                b -= 1
            elif r > 0:
                spies[pos] = 2
                r -= 1
                
def newGame():
    try: 
        request.query['newgame']
        if gameOver:
            setupMatch()
    except:
        pass

def checkAccount():
    ip = request['REMOTE_ADDR']
    if not ip in playerDict:
        playerDict[ip] = random.choice(wordList)
        if len(teams['blue']) <= len(teams['red']):
            teams['blue'].append(ip)
        else:
            teams['red'].append(ip)
    return ip 

def listPlayers(teamanme=None):
    if teamanme == None:
        if blue_first:
            return listPlayers('blue') + listPlayers('red')
        else:
            return listPlayers('red') + listPlayers('blue')
    else:
        players = ""
        for ip in teams[teamanme]:
            players += "<span class='" + getPlayerClass(ip) + "'>"+playerDict[ip]+"</span>&nbsp;"
        return players
    
def getWordHtml():
    ip = checkAccount()
    isMaster = ip in spymasters
    wordhtml = [""]*deckSize
    for i in range(len(spies)):
        wordColour = ""
        if spies[i] == -1: wordColour = "black"
        elif spies[i] == 0: wordColour = "gray"
        elif spies[i] == 1: wordColour = "blue"
        elif spies[i] == 2: wordColour = "red"
        wordbase = wordsSample[i]
        if revealed[i]:
            wordclass = "hidden-" + wordColour + " revealed-" + wordColour
        elif isMaster or gameOver:
            wordclass = "hidden-" + wordColour 
        else:
            wordclass = "hidden"
            wordbase = "<a href='/?reveal=" + str(i) + "'>" + wordbase + "</a>"        
        wordhtml[i] = "<td class='" + wordclass + "'>" + wordbase + "</td>"    
    return wordhtml

def gameOverScreen():
    if not gameOver:
        return ""
    else:
        return "<h2 class='account'><a href='/?newgame=1'>Νέα παρτίδα</a></h2>"

def revealWord():
    global revealed
    ip = checkAccount()
    try:
        word = int(request.query['reveal'])
        if not gameOver and not ip in spymasters and not revealed[word]:
            revealed[word] = True
            checkGameOver()
    except:
        pass
    
def checkGameOver():
    global gameOver
    redDone = True
    blueDone = True
    for i in range(len(spies)):
        if not revealed[i]:
            if spies[i] == 1:
                blueDone = False
            elif spies[i] == 2:
                redDone = False
        elif spies[i] == -1:
            gameOver = True
    if redDone or blueDone:
        gameOver = True
        
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/')

@route('/')
def main():
    ip = checkAccount()
    newGame()
    revealWord()    
    return template('main', username = playerDict[ip], word = getWordHtml(), players=listPlayers(), gameoverscreen = gameOverScreen())

@route('/account')        
def account():    
    ip = checkAccount()
    accountTeam = getTeam(ip)
    blue = "checked" if accountTeam == 'blue' else ""
    red =  "checked" if accountTeam == 'red' else ""
    master = "checked disabled='true'" if ip in spymasters else ""
    return template('account', ipaddress = ip, username = playerDict[ip], checkedBlue = blue, checkedRed = red, spymaster = master)
            
@route('/account', method='POST')
def account_post():
    try:
        #gather original info:
        ip = request['REMOTE_ADDR']
        oldTeam = getTeam(ip)
        #gather changed  info
        newTeam = request.forms.get('team')
        newName = request.forms.get('username')
        isMaster = not request.forms.get('spymaster') is None
        #save new info:
        if len(newName) > 0: playerDict[ip] = newName
        else: raise #μπράβο Παύλε μεγάλε τέστερ και καραμπουζουκλή!!
        if not newTeam == oldTeam:
            teams[oldTeam].remove(ip)
            teams[newTeam].append(ip)
        if isMaster:
            spymasters.append(ip)
        return "<a href='/'>Οι αλλαγές αποθηκεύτηκαν!</a>"
    except:     
        return "<a href='/account'>Προέκυψε κάποιο πρόβλημα!</a>"

setupMatch()    
run(host='0.0.0.0', port=8080, debug=True)