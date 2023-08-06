from random import *

initInputInfo = 'Guess a number: '
initRightInfo = 'Right'
initLowInfo = 'too low'
initHighInfo = 'too high'

def GuessNumGame(startNum, endNum, inputInfo = initInputInfo, rightInfo = initRightInfo, lowInfo = initLowInfo, highInfo = initHighInfo):

    num = randint(startNum, endNum)
    guessTimes = 0

    while True:
        guessNum = int(input(inputInfo))
        guessTimes += 1

        if num == guessNum:
            print(rightInfo)
            break
        elif num > guessNum:
            print(lowInfo)
        elif num < guessNum:
            print(highInfo)
    return guessTimes

#test
#a = GuessNumGame(1, 5, '猜一个1-5的数字：', '对了', '低了', '高了')
#print(a)
