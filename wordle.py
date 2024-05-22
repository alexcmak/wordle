from enum import Enum
import random
import math


class GuessResult(Enum):
    EXACT_CORRECT = 1
    APPEAR_WRONG_POSITION = 2
    NOT_APPEAR_AT_ALL = 3


fiveletterwords = []


def readWordList(fileName):
    try:
        print(f"reading file {fileName}")
        with open(fileName, "r") as f:
            for line in f:
                fiveletterwords.append(line.rstrip("\n"))
    except IOError:
        print("Error: This game requires the 5 letter word list")


def getGuessWord():
    num = random.random()
    random_int = math.floor(num * len(fiveletterwords))
    return fiveletterwords[random_int]


def readWordFromUser():
    isValidWord = False
    str = ""
    while not isValidWord:
        str = input(f"Please guess a {MAX} letter word:")

        if len(str) != MAX:
            print(f"You must enter a {MAX} letter word")
            continue
        else:
            if not str in fiveletterwords:
                print(f"You must enter a valid {MAX} letter word")
                continue

        return str


def evaluateGuess(wordToGuess, userGuess):
    result = [None] * MAX
    guessWordArray = list(wordToGuess)
    # char[] guessWordArray = wordToGuess.toCharArray();

    for i in range(MAX):
        if wordToGuess[i] == userGuess[i]:
            result[i] = GuessResult.EXACT_CORRECT
            guessWordArray[i] = " "

    for i in range(MAX):
        # //System.out.println("i="+i);

        if result[i] == GuessResult.EXACT_CORRECT:
            continue

        found = False
        for j in range(MAX):
            # print(f"comparing {userGuess[i]} vs {guessWordArray[j]}");
            if userGuess[i] == guessWordArray[j]:
                result[i] = GuessResult.APPEAR_WRONG_POSITION
                guessWordArray[j] = " "
                found = True
                break

        if not found:
            # System.out.println( choice.charAt(i)+": GRAY");
            result[i] = GuessResult.NOT_APPEAR_AT_ALL

    return result


def showGuessResult(choice, guessResult):
    for i in range(MAX):
        color = ""
        r = guessResult[i]
        if r == GuessResult.EXACT_CORRECT:
            color = "GREEN"
        elif r == GuessResult.APPEAR_WRONG_POSITION:
            color = "ORANGE"
        elif r == GuessResult.NOT_APPEAR_AT_ALL:
            color = "GREY"
        print(f"{choice[i]} : {color}")


MAX = 5
MAX_TRIALS = 6


def main():
    readWordList("words5.txt")

    guessWord = getGuessWord()
    gameOver = False
    trial = 1

    while not gameOver:
        print(f"Trial {trial}")
        # print("shh, it is: "+guessWord);

        choice = readWordFromUser()

        if choice == guessWord:
            print("You won!")
            break

        guessResult = evaluateGuess(guessWord, choice)
        showGuessResult(choice, guessResult)
        trial = trial + 1
        if trial > MAX_TRIALS:
            print("Sorry you lost, the word is: " + guessWord)
            gameOver = True


if __name__ == "__main__":
    main()
