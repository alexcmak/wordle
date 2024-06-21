from enum import Enum
import sqlite3

'''
This is a simple implementation of the Wordle game from New York Times.
You have 6 chances to guess a 5 letter word.
Each guess must be a real English word. I have a list of 5 letter words in a database.

If you guess exactly correct letter and correct position you get a green color.
If you guess right letter but wrong position you get a orange color.
If you guess a totally not appear letter you get a grey color.
'''

MAX = 5
MAX_TRIALS = 6

class GuessResult(Enum):
    EXACT_CORRECT = 1
    APPEAR_WRONG_POSITION = 2
    NOT_APPEAR_AT_ALL = 3


def getGuessWord(conn):
    
    # select word from Dictionary
    sql = "select word FROM dictionary order by random() limit 1;"

    cursor = conn.execute(sql)
    word = cursor.fetchone()
    return word[0]


def readWordFromUser(conn):
    isValidWord = False
    str = ""
    while not isValidWord:
        str = input(f"Please guess a {MAX} letter word:")

        if len(str) != MAX:
            print(f"You must enter a {MAX} letter word")
            continue
        else:
            sql = "select count(*) from dictionary where word = '" + str + "'"
            cursor = conn.execute(sql)
            count = cursor.fetchone()[0]
    
            if count == 0:
                print(f"You must enter a valid {MAX} letter word")
                continue

        return str


def evaluateGuess(wordToGuess, userGuess):
    result = [None] * MAX
    guessWordArray = list(wordToGuess)

    for i in range(MAX):
        if wordToGuess[i] == userGuess[i]:
            result[i] = GuessResult.EXACT_CORRECT
            guessWordArray[i] = " "

    for i in range(MAX):

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
            result[i] = GuessResult.NOT_APPEAR_AT_ALL

    return result

def green_letter(letter):
     return ('\x1b[6;30;42m' + letter + '\x1b[0m')
        
def orange_letter(letter):
    return ('\x1b[1;30;103m' + letter + '\x1b[0m')

def grey_letter(letter):
    return ('\x1b[1;97;100m' + letter + '\x1b[0m')

def showGuessResult(choice, guessResult):
    for i in range(MAX):
        color = ""
        r = guessResult[i]
        letter = choice[i].upper()

        if r == GuessResult.EXACT_CORRECT:
            color = "GREEN"
            colored_text = green_letter(letter)
        elif r == GuessResult.APPEAR_WRONG_POSITION:
            color = "ORANGE"
            colored_text = orange_letter(letter)
        elif r == GuessResult.NOT_APPEAR_AT_ALL:
            color = "GREY"
            colored_text = grey_letter(letter)

        print(colored_text, end='')
  
    print()

def main():

    gameOver = False
    trial = 1

    try:
        conn = sqlite3.connect('wordle.db3')
        guessWord = getGuessWord(conn)

        while not gameOver:
            print(f"Trial {trial}")
            #print("shh, it is: "+guessWord);

            choice = readWordFromUser(conn)

            if choice == guessWord:
                result = [None] * MAX
                for i in range(0, MAX):
                    result[i] = GuessResult.EXACT_CORRECT

                showGuessResult(choice, result)
                print("You won!")
                break

            guessResult = evaluateGuess(guessWord, choice)
            showGuessResult(choice, guessResult)
            trial = trial + 1
            if trial > MAX_TRIALS:
                print("Sorry you lost, the word is: " + guessWord)
                gameOver = True

        
    except sqlite3.Error as error:
        print('Program failed: ', error)
        return

    conn.close()

if __name__ == "__main__":
    main()
