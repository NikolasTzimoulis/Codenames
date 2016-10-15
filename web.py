# -*- coding: utf-8 -*- 
from bottle import route, run, request, template
import random 

wordFile = 'words-el.txt'

deckSize=25
playerDict = {}
wordList = []
for word in open(wordFile, 'r'):
    wordList.append(word)
wordsSample = []
    
def setupMatch():
    global wordsSample, blue_first
    wordsSample = random.sample(wordList, deckSize)
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

def checkAccount():
    ip = request['REMOTE_ADDR']
    if not ip in playerDict:
        playerDict[ip] = random.choice(wordList)
    return ip 

@route('/')
def main():
    ip = checkAccount()    
    return template('main', username = playerDict[ip], word = wordsSample)

@route('/account')        
def account():    
    ip = checkAccount()
    return """<p>IP: """ + ip + """</p>
            <form action='/account' method='post'> 
            <p>Όνομα: <input name='username' type='text' value='""" + playerDict[ip] + """'/></p>
            <p><input value='Αποθήκευση' type='submit' /></p></form>"""
            
@route('/account', method='POST')
def account_post():
    try:
        ip = request['REMOTE_ADDR']
        newname = request.forms.get('username')
        print newname
        playerDict[ip] = newname
        return "<a href='/'>Οι αλλαγές αποθηκεύτηκαν!</a>"
    except:     
        return "<a href='/account'>Προέκυψε κάποιο λάθος!</a>"

setupMatch()    
run(host='0.0.0.0', port=8080, debug=True)