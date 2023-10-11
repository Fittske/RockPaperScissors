import sys
from beautifultable import BeautifulTable
import random
import hmac
import hashlib
import os

class Help:  
    def __init__(self, turns):
        self.turns = turns
    def table(self):
        header=["v PC\\User >"]
        for i in turns:
            header.append(i)
        table = BeautifulTable()
        table.columns.header = header

        for idx, i in enumerate(turns):
            row = []
            row.append(i)
            for idx2, j in enumerate(turns):
                if idx2 == idx:
                    row.append('DRAW')
                elif idx > idx2:
                    if idx - idx2 > (len(turns)-1)/2:
                        row.append('WIN')
                    else:
                        row.append('LOSE')
                elif idx2 > idx:
                    if idx2 - idx > (len(turns)-1)/2:
                        row.append('LOSE')
                    else:
                        row.append('WIN')
            table.rows.append(row)
        print('Results are from user point of view:')
        print(table)

# Key generation and PC turn imitation
class KeyGeneration:
    def __init__(self, turns):
        self.turns = turns
    def generation(self):
        # 1. Generation of 256-bit secret key.
        key = os.urandom(32)
        
        # 2. Generation of PC turn.
        pcTurn = random.choice(turns)
        message = pcTurn.encode()
        
        return key, message
       
class HMACGeneration:
    def __init__(self, turns, key, message):
        self.turns = turns
        self.key = key
        self.message = message
    def generation(self):
        # 3. Generation of HMAC from key and message.
        hmacFin = hmac.new(key, message, hashlib.sha256).hexdigest()
        return hmacFin

class WinnerDetermination:
    def __init__(self, turns, userTurn, pcTurn):
        self.turns = turns
        self.userTurn = userTurn
        self.pcTurn = pcTurn
    def determination(self):
        idxUser = turns.index(userTurn)
        idxPC = turns.index(pcTurn)
        
        if idxUser == idxPC:
            result = 'Draw!'
        elif idxUser > idxPC:
            if idxUser-idxPC > (len(turns)-1)/2:
                result = 'You lose!'
            else:
                result = 'You win!'     
        elif idxUser < idxPC:
            if idxPC-idxUser > (len(turns)-1)/2:
                result = 'You win!'
            else:
                result = 'You lose!' 
        return result

turns = sys.argv[1:]
if (len(turns) < 3):
    print('The number of arguments should be at least 3!\n'
          'For Example:\n'
          'Rock Paper Scissors')
    exit()
elif (len(turns) % 2 == 0):
    print('The number of arguments should be odd!\n'
          'For Example:\n'
          '1. Rock Paper Scissors\n'
          '2. Rock Paper Scissors Lizard Spock\n'
          '3. Rock Paper Scissors Lizard Spock 6th 7th\n')
    exit()
elif (len(turns) > len(set(turns))):
    print('Argument values must be unique!')
    exit()
else:
    keyGen = KeyGeneration(turns)
    key, message = keyGen.generation()

    hmacGen = HMACGeneration(turns, key, message)
    hmacFin = hmacGen.generation()

    print('HMAC: ' + hmacFin.upper())
    print('Available moves:')
    for idx, i in enumerate(turns):
        print(f'{idx+1} - {i}')       
    print('0 - exit\n? - help')


isInputLeadForward = False
while isInputLeadForward != True:
    userTurnStr = str(input("Enter your move: "))
    if userTurnStr == '0':
        exit()
    elif userTurnStr == '?':
        help = Help(turns)
        help.table()
    else:
        isInputLeadForward = True
        userTurn = turns[int(userTurnStr)-1]
        pcTurn = message.decode()
        print('Your move: ' + userTurn)
        print('Computer move: ' + pcTurn)
    

winnerDet = WinnerDetermination(turns, userTurn, pcTurn)
result = winnerDet.determination()
print(result)
print('HMAC key: ' + key.hex().upper())
