from utils.utilities import waitFindInputAndSendKeys, waitFindAndReturn, waitFindAndClick, clearChat, filterBmp
from selenium.webdriver.common.by import By
from command_modules.korniszon_module.leaderboard import Leaderboard
import random

def check_symbol(symbol):
    vowels = "aeiouyąęóAEIOUYĄĘÓ"

    if symbol.isdigit():
        return "Number"
    elif symbol.isalpha():
        if symbol in vowels:
            return 'Vowel'
        else:
            return "Letter"
    elif symbol == " ":
        return "Space"
    
    else:
        return "Other"
    
def korniszon_cleanup(driver, korniszon_text):

    korniszon_text = korniszon_text.lower() # make words lowercase so they look better
    korniszon_text = korniszon_text.rstrip() # remove spaces after string, so there are no doubles counted as diffrent word with spaces at the end
    korniszon_text = ''.join([char for char in korniszon_text if char.isalpha() or char == " "]) # clear the word from anything else than letters and spaces
    
 
    return korniszon_text
    
    
def score_characters_value(score, korniszon_text):
    for char in korniszon_text:

        if check_symbol(char) == 'Letter' or 'Vowel' or "Space":
            rand = random.randint(9, 15)
            char_score = ord(char) % rand
            score += char_score * 2
    
    score = score / len(korniszon_text)

    score /= 2.413 # tuning
    score *= random.uniform(1, 1.06) # grain of randomness
    score *= 10 # to make it look nicer

    return round(score, 2)


def score_vowels_percent(score, korniszon_text):

    vowels_count = 0
    vowels_percent = 0


    for char in korniszon_text:
        if check_symbol(char) == 'Vowel':
            vowels_count += 1

    vowels_percent = vowels_count / len(korniszon_text) * 100
    print(f"{vowels_percent} = {vowels_count} / {len(korniszon_text)} * 100 ")

    if vowels_percent <= 50 and vowels_percent >= 20:
        score *= 2

    elif vowels_percent <= 75 and vowels_percent >= 10:
        score *= 1
        
    else:
        score *= 0
    
    print(f"Vowels: {vowels_percent}%")

    return round(score, 2)


def score_repetitions(score, korniszon_text):

    chars_reps = []

    for char in korniszon_text:

        if char not in chars_reps:
            chars_reps.append(char)

            if check_symbol(char) != 'Vowel':

                if korniszon_text.count(char) > 2: # do it only if there are alot of repetitions

                    repetitions = korniszon_text.count(char) / 2
                    score /= repetitions

                    print(f"{char}: {score} / {repetitions}")
    
    return round(score, 2)


def score_lenght(score, korniszon_text):
    
    lenght = len(korniszon_text)
    rand = random.randint(5, 10)
    golden_lenght = rand # the best number of letters for a korniszon
    diffrence = abs(golden_lenght - lenght)
    diffrence_halved = diffrence / 4

    #avoid dividing by 0
    if diffrence_halved > 0:
        score /= diffrence_halved

    return round(score, 2)


def send_results(driver, score, korniszon_text, position):
    emotka = ""

    if score > 500:
        emotka = "! :o"
    elif score > 300:
        emotka = "! <hura>"
    elif score > 200:
        emotka = "! :>"
    elif score > 150:
        emotka = ". ;>"
    elif score == 131.72:
        emotka = ". :))"
    elif score > 100:
        emotka = ". <myśli>"
    elif score == 21.37:
        emotka = ". <lol>"
    elif score > 75:
        emotka = ".. :/"
    elif score > 50:
        emotka = ".. <palacz>"
    elif score > 0:
        emotka = "... ;("
    elif score == 00.10:
        emotka = "... <leje>"
    elif score == 0:
        emotka = "..... <idiota>"            

    response = (f"{korniszon_text} zdobył {score} punktów{emotka}\n"
    f"Zajął {position} miejsce.")
    waitFindInputAndSendKeys(driver, 10, By.ID, "chat-text", response)
    



#---------------
# main def
def korniszon(driver, korniszon_text, leaderboard):

    score = 0

    # so it doesn't take the same word again
    clearChat(driver)

    # remove special chars, numbers etc, so it looks nice no matter how much user (fircyk) is trying to make it ugly ;>   
    korniszon_text = korniszon_cleanup(driver, korniszon_text)

    # leaderboard = Leaderboard()
    leaderboard.load_leaderboard()

    # if duplicates
    # print(f"Korniszon: {korniszon_text} in {leaderboard.leaderboard}")
    if korniszon_text in leaderboard.leaderboard:

        pozycja = leaderboard.get_position(korniszon_text)
        response = f"{korniszon_text} już jest na pozycji {pozycja}. Wymyśl nowego korniszona <okok>"
        return waitFindInputAndSendKeys(driver, 10, By.ID, "chat-text", response)
    

    # in case there were no letters in korniszon and you were left with empty variable
    if len(korniszon_text) == 0:

        response = f"{random.randint(-784545, -3456)} punktów <zniesmaczony>. Naum się w korniszony!"
        return waitFindInputAndSendKeys(driver, 10, By.ID, "chat-text", response)
    
    elif len(korniszon_text) > 30:
        response = "Nie będę oceniał takiego długasa <nono>"
        return waitFindInputAndSendKeys(driver, 10, By.ID, "chat-text", response)
    
    

    # check each character unicode number and then modulo them to get some random numbers, I want to make it hard to predict
    score = score_characters_value(score, korniszon_text)
    print(f"Char score: {round(score, 2)}")
    print('---')

    # check how many % of the string are vowels and then multiple the score - accoring to set rules. 
    # I don't want korniszons to have too many or too less vowels so they still sounds like words, ~30% is an golden rule.
    score = score_vowels_percent(score, korniszon_text)
    print(f"Vowels score: {round(score, 2)}")
    print('---')

    #score repetitions
    # check every character in a string ONCE, for how many repetitions it has and then divide the score by it
    # i don't want too many the same letters in one word to avoid fgddfdgfgfff  
    score = score_repetitions(score, korniszon_text)
    print(f"Reps score: {round(score, 2)}")
    print('---')

    # to avoid too short or too long words, the bigger diffrence from the ideal lenght the worse score
    score = score_lenght(score, korniszon_text)
    print(f"Len score: {round(score, 2)}")
    print('---')


    # add new position to leaderboard, do it after calculating score
    leaderboard.new_korniszon(korniszon_text, score)

    # send the message on gg how much point your korniszon earned and what position it has on leaderbord
    position = leaderboard.get_position(korniszon_text)

    send_results(driver, score, korniszon_text, position)
    print(f"Full score: {round(score, 2)}")

            










